from rest_framework.serializers import SerializerMethodField, ModelSerializer

from .models import Ingredient, RecipeIngredients, Recipe, Tag
from api.models import User


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["name", "measurement_unit"]


class RecipeIngredientsSerializer(ModelSerializer):
    id = SerializerMethodField()
    name = SerializerMethodField()
    measurement_unit = SerializerMethodField()

    class Meta:
        model = RecipeIngredients
        fields = ["id", "name", "amount", "measurement_unit"]

    def get_id(self, obj):
        return obj.ingredient.id

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class RecipeSerializer(ModelSerializer):
    ingredients = RecipeIngredientsSerializer(many=True)
    author = AuthorSerializer()

    class Meta:
        model = Recipe
        fields = "__all__"
        depth = 1


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "color", "slug"]
