from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import (GenericViewSet, ModelViewSet,
                                     ReadOnlyModelViewSet)
from wkhtmltopdf.views import PDFTemplateResponse

from users.models import User

from .filters import RecipeFilter
from .models import (Ingredient, Recipe, RecipeFavourite,
                     RecipeIngredientsDetails, RecipeShoppingCart, Tag,
                     UserFollow)
from .permissions import IsAuthorOrIsStaffOrReadOnly
from .serializers import (CustomUserSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RecipeFavouriteSerializer,
                          RecipeReadSerializer, ShoppingCartSerializer,
                          TagSerializer, UserFollowSerializer)


class IngredientViewSet(ReadOnlyModelViewSet):
    """Получение ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (SearchFilter,)
    search_fields = ("name",)


class RecipeViewSet(ModelViewSet):
    """Создание, получение и удаление рецептов."""
    queryset = Recipe.objects.all().order_by("-pub_date")
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAuthorOrIsStaffOrReadOnly)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return RecipeReadSerializer
        return RecipeCreateSerializer


class TagViewSet(ReadOnlyModelViewSet):
    """Получение тегов."""
    pagination_class = None
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeUserRelationsViewSet(GenericViewSet, CreateModelMixin,
                                 RetrieveModelMixin,
                                 DestroyModelMixin):
    """
    Добавление и удаление модели, связывающей модели User и Recipe.
    Необходимо добавить queryset, serializer_class
    и переопределить класс Meta (model, fields).
    """
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        data = request.data
        data["user"] = request.user.id
        data["recipe"] = kwargs.get("recipe_id")

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(self.Meta.model,
                                     user=request.user.id,
                                     recipe=kwargs.get("recipe_id"))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeFavouriteViewSet(RecipeUserRelationsViewSet):
    """Добавление рецепта в избранное и удаление рецепта из избранного."""
    queryset = RecipeFavourite.objects.order_by("-recipe__pub_date")
    serializer_class = RecipeFavouriteSerializer

    class Meta:
        model = RecipeFavourite


class ShoppingCartViewSet(RecipeUserRelationsViewSet,
                          ListModelMixin):
    """Добавление и удаление рецепта из списка покупок."""
    queryset = RecipeShoppingCart.objects.order_by("-recipe__pub_date")
    serializer_class = ShoppingCartSerializer

    class Meta:
        model = RecipeShoppingCart

    def get_purchases(self, request):
        """
        Возвращает список покупок.
        Список ингредиентов формируется из ингредиентов, имеющихся
        во всех добавленных в список покупок рецептов, без повторения
        одинаковых ингредиентов.
        """
        shopping_cart = RecipeShoppingCart.objects.filter(user=request.user)
        purchases = {}
        for cart in shopping_cart:
            recipe_ingredients = RecipeIngredientsDetails.objects.filter(
                recipe=cart.recipe)
            for recipe_ingredient in recipe_ingredients:
                name = (f"{recipe_ingredient.ingredient.name} "
                        f"({recipe_ingredient.ingredient.measurement_unit})")
                amount = recipe_ingredient.amount
                if name in purchases:
                    purchases[name] += amount
                else:
                    purchases[name] = amount
        return purchases

    def list(self, request, *args, **kwargs):
        """
        Возвращает список ингредиентов, которые необходимо купить, в виде
        pdf-файла. """

        template = get_template("shopping_cart.html")
        return PDFTemplateResponse(
            request=request,
            template=template,
            filename="shopping_cart.pdf",
            context={"purchases": self.get_purchases(request)},
            show_content_in_browser=False,
            cmd_options={'margin-top': 50, },
        )


class SubscriptionsViewSet(ModelViewSet):
    """Управление подпиской на пользователя."""
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return CustomUserSerializer
        return UserFollowSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(followers__user=user).order_by("id")

    def create(self, request, *args, **kwargs):
        data = request.data
        data["user"] = request.user.id
        data["follow_to"] = kwargs.get("author_id")

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(UserFollow,
                                     user=request.user.id,
                                     follow_to=kwargs.get("author_id"))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
