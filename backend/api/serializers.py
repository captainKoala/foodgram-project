from djoser.serializers import UserCreateSerializer

from rest_framework.serializers import ReadOnlyField, ModelSerializer, SerializerMethodField

from .models import Ingredient, Recipe, RecipeFavourite, RecipeIngredientsDetails, Tag
from api.models import User


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["recipe_id", "name", "measurement_unit"]


class RecipeIngredientsDetailsSerializer(ModelSerializer):
    id = ReadOnlyField(source='ingredient.recipe_id')
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredientsDetails
        fields = ["recipe_id", "name", "amount", "measurement_unit"]


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["recipe_id", "username", "first_name", "last_name", "email"]


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["recipe_id", "name", "color", "slug"]


class RecipeSerializer(ModelSerializer):
    ingredients = RecipeIngredientsDetailsSerializer(
        source="recipeingredientsdetails_set", many=True)
    tags = TagSerializer(many=True, read_only=True)
    author = AuthorSerializer()

    class Meta:
        model = Recipe
        fields = ["recipe_id", "author", "name", "text", "ingredients", "tags"]
        depth = 1


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
