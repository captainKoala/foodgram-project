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

from .models import Ingredient, Recipe, RecipeFavourite, RecipeIngredientsDetails, Tag
from .permissions import IsAuthorOrReadOnly
from .serializers import IngredientSerializer, RecipeSerializer, RecipeFavouriteSerializer, TagSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [SearchFilter]
    search_fields = ['name']


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all().order_by("id")
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def create(self, request, *args, **kwargs):
        data = request.data

        tag_ids = data.pop("tags")
        tags = []
        for tag_id in tag_ids:
            try:
                tag = Tag.objects.get(id=tag_id)
            except Tag.DoesNotExist:
                raise ValidationError({
                    "detail": "Тег с указанным recipe_id не найден."})
            tags.append(tag)

        rec_ingredients_data = data.pop("ingredients")

        data["author_id"] = request.user.id

        recipe = Recipe(**data)

        ingredients = []
        rec_ingredients = []
        for rec_ingredient_id in rec_ingredients_data:
            try:
                ingredient = Ingredient.objects.get(id=rec_ingredient_id["recipe_id"])
            except KeyError:
                raise ValidationError({
                    "detail": "Необходимо указать recipe_id ингридиента."})
            except Ingredient.DoesNotExist:
                raise ValidationError({
                    "detail": "Ингредиент с указанным recipe_id не найден."})
            amount = rec_ingredient_id.get("amount")
            if amount is None:
                raise ValidationError({
                    "detail": "Значение amount не передано."})
            ingredients.append(ingredient)
            rec_ingredients.append(RecipeIngredientsDetails(
                recipe=recipe,
                ingredient=ingredient,
                amount=amount)
            )
        recipe.save()
        RecipeIngredientsDetails.objects.bulk_create(rec_ingredients)

        recipe.tags.set(tags)
        recipe.ingredients.set(ingredients)

        serializer = self.get_serializer(recipe)

        return Response(serializer.data)


class TagViewSet(ReadOnlyModelViewSet):
    pagination_class = None
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


def index(request):
    last_recipes = Recipe.objects.order_by("pub_date")
    return HttpResponse("Hello world!")


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
        return JsonResponse({"recipe_id": favourite.id,
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
