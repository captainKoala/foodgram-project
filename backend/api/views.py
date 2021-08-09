from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.decorators import api_view
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
                          RecipeCreateSerializer,
                          RecipeIngredientsDetailsCreateSerializer,
                          RecipeIngredientsDetailsReadSerializer,
                          RecipeFavouriteSerializer, RecipeReadSerializer,
                          ShoppingCartSerializer, TagSerializer)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (SearchFilter, )
    search_fields = ("name", )


class RecipeIngredientDetailsViewSet(ModelViewSet):
    queryset = RecipeIngredientsDetails.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return RecipeIngredientsDetailsReadSerializer
        return RecipeIngredientsDetailsCreateSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all().order_by("-pub_date")
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAuthorOrIsStaffOrReadOnly)
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return RecipeReadSerializer
        return RecipeCreateSerializer


class TagViewSet(ReadOnlyModelViewSet):
    pagination_class = None
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeUserRelationsCreateDestroyViewSet(GenericViewSet, CreateModelMixin,
                                              RetrieveModelMixin,
                                              DestroyModelMixin):
    """
    Добавление и удаление модели, связывающей модели User и Recipe.
    Необходимо добавить queryset, serializer_class
    и переопределить класс Meta (model, fields).
    """
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticated, )

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


class RecipeFavouriteViewSet(RecipeUserRelationsCreateDestroyViewSet):
    """Добавление рецепта в избранное и удаление рецепта из избранного."""
    queryset = RecipeFavourite.objects.order_by("-recipe__pub_date")
    serializer_class = RecipeFavouriteSerializer

    class Meta:
        model = RecipeFavourite


class ShoppingCartViewSet(RecipeUserRelationsCreateDestroyViewSet,
                          ListModelMixin):
    """Добавление и удаление рецпта из списка покупок."""
    queryset = RecipeShoppingCart.objects.order_by("-recipe__pub_date")
    serializer_class = ShoppingCartSerializer

    class Meta:
        model = RecipeShoppingCart

    def list(self, request, *args, **kwargs):
        """
        Возвращает список ингредиентов, которые необходимо купить, в виде
        pdf-файла. Список ингредиентов формируется из ингредиентов, имеющихся
        во всех добавленных в список покупок рецептов, без повторения
        одинаковых ингредиентов."""
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

        template = get_template("shopping_cart.html")
        return PDFTemplateResponse(request=request,
                                   template=template,
                                   filename="shopping_cart.pdf",
                                   context={"purchases": purchases},
                                   show_content_in_browser=False,
                                   cmd_options={'margin-top': 50, },
                                   )

@api_view(["GET", "DELETE"])
def subscribe(request, author_id):
    author = get_object_or_404(User, id=author_id)
    user = request.user

    if author == user:
        return Response({"errors": "Нельзя подписаться на себя"},
                        status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        try:
            UserFollow.objects.create(user=user, follow_to=author)
        except IntegrityError:
            return Response(
                {"errors": "Вы уже подписаны на этого пользователя"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = CustomUserSerializer(user, context={"request": request})
        return Response(serializer.data)

    # DELETE
    subscription = get_object_or_404(UserFollow, user=user, follow_to=author)
    subscription.delete()
    return Response({"detail": "Подписка отменена"},
                    status=status.HTTP_204_NO_CONTENT)


class SubscriptionsViewSet(ReadOnlyModelViewSet):
    pagination_class = PageNumberPagination
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(followers__user=user)
