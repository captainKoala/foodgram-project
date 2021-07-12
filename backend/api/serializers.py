from rest_framework.serializers import ReadOnlyField, ModelSerializer, SerializerMethodField

from .models import Ingredient, RecipeIngredientsDetails, Recipe, Tag
from api.models import User


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name", "amount", "measurement_unit"]


class RecipeIngredientsDetailsSerializer(ModelSerializer):
    id = ReadOnlyField(source='ingredient.id')
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredientsDetails
        fields = ["id", "name", "amount", "measurement_unit"]


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "color", "slug"]


class RecipeSerializer(ModelSerializer):
    ingredients = RecipeIngredientsDetailsSerializer(source="recipeingredientsdetails_set", many=True)
    tags = TagSerializer(many=True)
    author = AuthorSerializer()

    class Meta:
        model = Recipe
        fields = ["id", "author", "name", "text", "ingredients", "tags"]
        depth = 1

    # def to_internal_value(self, data):
    #     data["author"] = self.context.get('request').user
    #     return data
    #

