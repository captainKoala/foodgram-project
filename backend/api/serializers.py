from rest_framework.serializers import ModelSerializer

from .models import Ingredient, Recipe, Tag


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name", "measurement_unit"]


class RecipeSerializer(ModelSerializer):
    class Meta:
        model = Recipe


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "color", "slug"]
