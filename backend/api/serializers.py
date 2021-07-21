from drf_extra_fields.fields import Base64ImageField

from djoser.serializers import UserCreateSerializer, UserSerializer

from rest_framework.serializers import ReadOnlyField, ModelSerializer, PrimaryKeyRelatedField, SerializerMethodField

from .models import (Ingredient, Recipe, RecipeFavourite,
                     RecipeIngredientsDetails, RecipeShoppingCart, Tag, User,
                     UserFollow)


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name", "measurement_unit"]

    def to_internal_value(self, data):
        return Ingredient.objects.get(id=data)


class RecipeIngredientsDetailsReadSerializer(ModelSerializer):
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


class RecipeReadSerializer(ModelSerializer):
    ingredients = RecipeIngredientsDetailsReadSerializer(
        source="recipeingredientsdetails_set", many=True)
    tags = TagSerializer(many=True, read_only=True)
    author = AuthorSerializer()
    image = Base64ImageField(max_length=None, use_url=True)
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ["id", "author", "name", "text", "ingredients", "tags",
                  "image", "cooking_time", "is_favorited",
                  "is_in_shopping_cart"]

    def get_is_favorited(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return RecipeFavourite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return RecipeShoppingCart.objects.filter(user=user,
                                                 recipe=obj).exists()


class RecipeCreateSerializer(ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientsDetailsCreateSerializer(many=True)
    image = Base64ImageField(max_length=None, use_url=True)
    author = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Recipe
        exclude = ["pub_date"]

    def create(self, validated_data):
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")

        recipe = Recipe.objects.create(**validated_data,
                                       author=self.context["request"].user)

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

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")

        instance.name = validated_data.get("name")
        instance.text = validated_data.get("text")
        instance.image = validated_data.get('image')
        instance.cooking_time = validated_data.get('cooking_time')
        instance.save()

        RecipeIngredientsDetails.objects.filter(recipe=instance).delete()

        instance.tags.set(tags)

        recipe_ingredients = []
        for ingredient in ingredients:
            recipe_ingredients.append(RecipeIngredientsDetails(
                recipe=instance,
                ingredient=ingredient["id"],
                amount=ingredient["amount"],
            ))
        RecipeIngredientsDetails.objects.bulk_create(recipe_ingredients)

        return instance

    def to_representation(self, instance):
        data = RecipeReadSerializer(
            instance,
            context={"request": self.context.get("request")}
        ).data
        return data


class RecipeReadShortSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ["id", "name", "image", "cooking_time"]


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name", "last_name"]


class CustomUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField()
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name",
                  "is_subscribed", "recipes", "recipes_count"]

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return UserFollow.objects.filter(user=user, follow_to=obj).exists()

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj).order_by("-pub_date")

        params = self.context.get("request").query_params
        recipes_limit = params.get("recipes_limit")
        if recipes_limit is not None:
            recipes_limit = int(recipes_limit)
            recipes = recipes[:recipes_limit]

        serializer = RecipeReadShortSerializer(
            recipes,
            many=True,
            context={"request": self.context.get("request")}
        )
        return serializer.data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()


class CustomUserShortSerializer(UserSerializer):
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name",
                  "is_subscribed",]

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return UserFollow.objects.filter(user=user, follow_to=obj).exists()
