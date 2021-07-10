from rest_framework.serializers import SerializerMethodField, ModelSerializer

from .models import Ingredient, RecipeIngredients, Recipe, Tag


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


class RecipeSerializer(ModelSerializer):
    ingredients = RecipeIngredientsSerializer(many=True)

    class Meta:
        model = Recipe
        fields = "__all__"
        depth = 1


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "color", "slug"]
