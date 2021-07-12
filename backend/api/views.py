from django.shortcuts import get_object_or_404

from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Ingredient, Recipe, RecipeIngredientsDetails, Tag
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all().order_by("id")
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        data = request.data

        tag_ids = data.pop("tags")
        tags = [get_object_or_404(Tag, id=tag_id) for tag_id in tag_ids]

        rec_ingredients_data = data.pop("ingredients")

        data["author_id"] = request.user.id

        recipe = Recipe.objects.create(**data)
        recipe.save()

        ingredients = []
        rec_ingredients = []
        for rec_ingredient_id in rec_ingredients_data:
            ingredient = Ingredient.objects.get(id=rec_ingredient_id["id"])
            amount = rec_ingredient_id["amount"]
            ingredients.append(ingredient)
            rec_ingredients.append(RecipeIngredientsDetails(
                recipe=recipe,
                ingredient=ingredient,
                amount=amount)
            )
        RecipeIngredientsDetails.objects.bulk_create(rec_ingredients)

        recipe.tags.set(tags)
        recipe.ingredients.set(ingredients)

        serializer = RecipeSerializer(recipe)

        return Response(serializer.data)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
