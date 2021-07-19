from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, HttpResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Ingredient, Recipe, RecipeShoppingCart, RecipeFavourite, RecipeIngredientsDetails, Tag
from .permissions import IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeListSerializer, TagSerializer,
                          RecipeIngredientsDetailsListSerializer,
                          RecipeIngredientsDetailsCreateSerializer)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [SearchFilter]
    search_fields = ['name']


class RecipeIngredientDetailsViewSet(ModelViewSet):
    queryset = RecipeIngredientsDetails.objects.all()
    # serializer_class = RecipeIngredientsDetailsListSerializer

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeIngredientsDetailsListSerializer
        return RecipeIngredientsDetailsCreateSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all().order_by("id")
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeListSerializer
        return RecipeCreateSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        data["author"] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TagViewSet(ReadOnlyModelViewSet):
    pagination_class = None
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


def index(request):
    last_recipes = Recipe.objects.order_by("pub_date")[:6]
    return HttpResponse()


@api_view(["POST", "DELETE"])
def recipe_favourites(request, recipe_id):
    user = request.user
    if user.is_anonymous:
        return Response({"detail": "Учетные данные не были предоставлены."},
                        status=status.HTTP_403_FORBIDDEN)
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.method == "POST":
        try:
            favourite = RecipeFavourite.objects.create(user=user, recipe=recipe)
        except IntegrityError:
            return Response({"errors": "Рецепт уже добавлен в избранное"},
                            status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({"id": favourite.id,
                             "name": recipe.name,
                             # "image": recipe.image.url,
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
        recipe_ingredients = RecipeIngredientsDetails.objects.filter(recipe=cart.recipe)
        for recipe_ingredient in recipe_ingredients:
            name = recipe_ingredient.ingredient.name
            amount = recipe_ingredient.amount
            if name in purchases:
                purchases[name] += amount
            else:
                purchases[name] = amount
    return Response(purchases)


@api_view(["POST", "DELETE"])
def manage_shopping_cart(request, recipe_id):
    user = request.user
    if user.is_anonymous:
        return Response({"detail": "Учетные данные не были предоставлены."},
                        status=status.HTTP_403_FORBIDDEN)
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.method == "POST":
        try:
            cart = RecipeShoppingCart.objects.create(user=user, recipe=recipe)
        except IntegrityError:
            return Response({"errors": "Рецепт уже добавлен в список покупок"},
                            status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({"id": cart.id,
                             "name": recipe.name,
                             # "image": recipe.image.url,
                             "cooking_time": recipe.cooking_time,
                             }, status=status.HTTP_201_CREATED
                            )
    # метод DELETE
    cart = get_object_or_404(RecipeShoppingCart, recipe=recipe, user=user)
    cart.delete()
    return Response({"detail": "Рецепт удален из списка покупок"},
                    status=status.HTTP_204_NO_CONTENT)
