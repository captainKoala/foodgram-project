from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from api.models import Ingredient, Tag, User

from . import data


class RecipesTestCase(APITestCase):
    def setUp(self):
        Tag.objects.create(**data.TAG_DATA_1)
        Tag.objects.create(**data.TAG_DATA_2)
        Ingredient.objects.create(**data.INGREDIENT_DATA_1)
        Ingredient.objects.create(**data.INGREDIENT_DATA_2)
        self.user_1 = User.objects.create(**data.USER_DATA_1)
        self.user_2 = User.objects.create(**data.USER_DATA_2)
        self.token_1 = Token.objects.create(user=self.user_1)
        self.authenticate()

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_1}")

    def test_create_recipe_without_token(self):
        self.client.credentials()
        response = self.client.post(data.RECIPES_URL, data.RECIPE_DATA_1)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            "Проверьте, что создание рецептов недоступно неавторизованному "
            "пользователю."
        )

    def test_create_recipe_with_token(self):
        response = self.client.post(data.RECIPES_URL, data.RECIPE_DATA_1)
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            "Проверьте, что при создании рецепта авторизованным пользователем "
            "возвращается статус 201."
        )
