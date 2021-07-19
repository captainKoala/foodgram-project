from djoser.serializers import UserCreateSerializer

from drf_extra_fields.fields import Base64ImageField

from rest_framework.serializers import ReadOnlyField, ModelSerializer, SerializerMethodField

from .models import Ingredient, Recipe, RecipeIngredientsDetails, Tag
from api.models import User


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name", "measurement_unit"]

    def to_internal_value(self, data):
        return Ingredient.objects.get(id=data)


class RecipeIngredientsDetailsListSerializer(ModelSerializer):
    id = ReadOnlyField(source='ingredient.id')
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredientsDetails
        fields = ["id", "name", "amount", "measurement_unit"]


class RecipeIngredientsDetailsCreateSerializer(ModelSerializer):
    id = IngredientSerializer()

    class Meta:
        model = RecipeIngredientsDetails
        fields = ["id", "amount"]


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "color", "slug"]

    def to_internal_value(self, data):
        return Tag.objects.get(id=data)


class RecipeListSerializer(ModelSerializer):
    ingredients = RecipeIngredientsDetailsListSerializer(
        source="recipeingredientsdetails_set", many=True)
    tags = TagSerializer(many=True, read_only=True)
    author = AuthorSerializer()
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Recipe
        fields = ["id", "author", "name", "text", "ingredients", "tags", "image"]


class RecipeCreateSerializer(ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientsDetailsCreateSerializer(many=True)
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = Recipe
        exclude = ["pub_date"]

    def create(self, validated_data):
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")

        recipe = Recipe.objects.create(**validated_data)

        recipe.tags.set(tags)

        recipe_ingredients = []
        for ingredient in ingredients:
            recipe_ingredients.append(RecipeIngredientsDetails(
                recipe=recipe,
                ingredient=ingredient["id"],
                amount=ingredient["amount"],
            ))
        RecipeIngredientsDetails.objects.bulk_create(recipe_ingredients)
        return recipe

    def to_representation(self, instance):
        data = RecipeListSerializer(
            instance,
            context={"request": self.context.get("request")}
        ).data
        return data


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
