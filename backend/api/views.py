from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from users.models import User

from .models import (Ingredient, Recipe, RecipeFavourite,
                     RecipeIngredientsDetails, RecipeShoppingCart, Tag,
                     UserFollow)
from .permissions import IsAuthorOrIsStaffOrReadOnly
from .serializers import (CustomUserSerializer, IngredientSerializer,
                          RecipeCreateSerializer,
                          RecipeIngredientsDetailsCreateSerializer,
                          RecipeIngredientsDetailsReadSerializer,
                          RecipeReadSerializer, TagSerializer)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [SearchFilter]
    search_fields = ['name']


class RecipeIngredientDetailsViewSet(ModelViewSet):
    queryset = RecipeIngredientsDetails.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeIngredientsDetailsReadSerializer
        return RecipeIngredientsDetailsCreateSerializer


class RecipeViewSet(ModelViewSet):
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsAuthorOrIsStaffOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeReadSerializer
        return RecipeCreateSerializer

    def get_queryset(self):
        queryset = Recipe.objects.all().order_by("-pub_date")
        user = self.request.user

        params = self.request.query_params
        tags = params.getlist("tags")
        is_favorited = params.get("is_favorited")
        is_in_shopping_cart = params.get("is_in_shopping_cart")
        author_id = params.get("author")

        if tags:
            queryset = queryset.filter(tags__slug__in=tags).distinct()
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        if is_favorited:
            queryset = queryset.filter(favourites__user=user)
        if is_in_shopping_cart:
            queryset = queryset.filter(to_shopping__user=user)

        return queryset


class TagViewSet(ReadOnlyModelViewSet):
    pagination_class = None
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


@api_view(["GET", "DELETE"])
def recipe_favourites(request, recipe_id):
    user = request.user
    if user.is_anonymous:
        return Response({"detail": "Учетные данные не были предоставлены."},
                        status=status.HTTP_403_FORBIDDEN)
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.method == "GET":
        try:
            favourite = RecipeFavourite.objects.create(user=user,
                                                       recipe=recipe)
        except IntegrityError:
            return Response({"errors": "Рецепт уже добавлен в избранное"},
                            status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({"id": favourite.id,
                             "name": recipe.name,
                             "image": recipe.image.url,
                             "cooking_time": recipe.cooking_time,
                             }, status=status.HTTP_201_CREATED
                            )
    # метод DELETE
    favourite = get_object_or_404(RecipeFavourite, recipe=recipe, user=user)
    favourite.delete()
    return Response({"detail": "Рецепт удален из избранного"},
                    status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def get_shopping_cart(request):
    user = request.user
    if user.is_anonymous:
        return Response({"detail": "Учетные данные не были предоставлены."},
                        status=status.HTTP_403_FORBIDDEN)
    shopping_cart = RecipeShoppingCart.objects.filter(user=user)
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
    text = "СПИСОК ПОКУПОК\n"
    for key, value in purchases.items():
        text += f"{key} - {value}\n"

    response = HttpResponse(text,
                            content_type="application/text charset=utf-8")
    response['Content-Disposition'] = ("attachment; "
                                       "filename=\"shopping-cart.txt\"")
    return response


@api_view(["GET", "DELETE"])
def manage_shopping_cart(request, recipe_id):
    user = request.user
    if user.is_anonymous:
        return Response({"detail": "Учетные данные не были предоставлены."},
                        status=status.HTTP_403_FORBIDDEN)
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.method == "GET":
        try:
            cart = RecipeShoppingCart.objects.create(user=user, recipe=recipe)
        except IntegrityError:
            return Response({"errors": "Рецепт уже добавлен в список покупок"},
                            status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({"id": cart.id,
                             "name": recipe.name,
                             "image": recipe.image.url,
                             "cooking_time": recipe.cooking_time,
                             }, status=status.HTTP_201_CREATED
                            )
    # метод DELETE
    cart = get_object_or_404(RecipeShoppingCart, recipe=recipe, user=user)
    cart.delete()
    return Response({"detail": "Рецепт удален из списка покупок"},
                    status=status.HTTP_204_NO_CONTENT)


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
