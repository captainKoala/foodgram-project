from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from users.models import User

from . import data


class UserCreateTestCase(APITestCase):
    def test_create_user(self):
        # ПРОВЕРКА СОЗДАНИЯ ПОЛЬЗОВАТЕЛЯ
        data_1 = data.USER_DATA_1
        response = self.client.post(data.USERS_URL, data_1, format="json")
        self.assertNotEqual(response.status_code,
                            status.HTTP_404_NOT_FOUND,
                            f"Проверьте, что адрес {data.USERS_URL} доступен."
                            )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            "Не удалось создать пользователя с корректными данными"
        )

        # ПРОВЕРКА СОЗДАНИЯ ПОЛЬЗОВАТЕЛЯ С УЖЕ СУЩЕСТВУЮЩИМ ИМЕНЕМ ПОЛЬЗОВАТЕЛЯ
        # ИЛИ E-MAIL
        data_2 = data_1.copy()
        data_2["username"] = "another_user"
        response = self.client.post(data.USERS_URL, data_2)
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST,
                         "Проверьте, что невозможно создать двух пользотелей "
                         "с одинаковым username.")
        data_2 = data_1.copy()
        data_2["email"] = "another_user@example.com"
        response = self.client.post(data.USERS_URL, data_2)
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST,
                         "Проверьте, что невозможно создать двух пользотелей "
                         "с одинаковым email.")

        # ПРОВЕРКА СОЗДАНИЯ ПОЛЬЗОВАТЕЛЕЙ С НЕПОЛНЫМИ ДАННЫМИ
        fields = data_1.keys()
        for field in fields:
            incomplete_data = data_1.copy()
            incomplete_data.pop(field)
            response = self.client.post(data.USERS_URL, incomplete_data,
                                        format="json")
            self.assertEqual(response.status_code,
                             status.HTTP_400_BAD_REQUEST,
                             f"Поле '{field}' обязательно для создания"
                             f"пользователя."
                             )


class UserTestCase(APITestCase):
    def setUp(self):
        self.user_1 = User.objects.create(**data.USER_DATA_1)
        self.user_2 = User.objects.create(**data.USER_DATA_2)
        self.token_1 = Token.objects.create(user=self.user_1)
        self.authenticate()

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_1}")

    def test_get_users_list(self):
        response = self.client.get(data.USERS_URL)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK,
                         f"Проверьте, что список пользователей доступен "
                         f"по адресу '{data.USERS_URL}' для "
                         f"авторизованного пользователя.")

        response_count = response.data.get("count")
        response_user_1_data = response.data.get("results")[0]

        # По ReDOC ожидаются поля email, id, username,
        # first_name, last_name, is_subscribed
        expected_user_data = data.USER_DATA_1.copy()
        expected_user_data.pop("password")
        expected_user_data["id"] = 1
        expected_user_data["is_subscribed"] = False
        self.assertEqual(response_count, User.objects.all().count(),
                         f"Проверьте, что в ответе на GET-запрос "
                         f"'{data.USERS_URL}' возвращается верное количество "
                         f"пользователей.")
        self.assertEqual(response_user_1_data, expected_user_data,
                         f"Проверьте, что в ответе на GET-запрос "
                         f"'{data.USERS_URL}' возвращаются верные данные о "
                         f"пользователе.")

    def test_get_user_by_id_with_token(self):
        user_id = 2
        url = f"{data.USERS_URL}{user_id}/"

        response = self.client.get(url)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK,
                         f"Проверьте, что авторизованному пользователю "
                         f"доступна страница '{data.USERS_URL}{{id}}'."
                         )

        response_user_data = response.data
        expected_user_data = data.USER_DATA_2.copy()
        expected_user_data.pop("password")
        expected_user_data["id"] = user_id
        expected_user_data["is_subscribed"] = False

        self.assertEqual(response_user_data, expected_user_data,
                         f"Проверьте, что в ответе на GET-запрос "
                         f"'{data.USERS_URL}{{id}}' возвращаются верные данные "
                         f"о пользователе.")

    def test_get_user_by_id_without_token(self):
        user_id = 2
        url = f"{data.USERS_URL}{user_id}/"

        self.client.credentials()
        response = self.client.get(url)
        # В ReDoc описан код 403 для неавторизованного пользователя,
        # но это видится неправильным
        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED,
                         f"Проверьте, что неавторизованному пользователю "
                         f"недоступна страница '{data.USERS_URL}{{id}}'."
                         )
        self.authenticate()

    def test_get_current_user_with_token(self):
        response = self.client.get(data.USERS_ME_URL)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK,
                         f"Проверьте, что авторизованному пользователю "
                         f"доступна страница '{data.USERS_ME_URL}'."
                         )

        response_user_data = response.data
        expected_user_data = data.USER_DATA_1.copy()
        expected_user_data.pop("password")
        expected_user_data["id"] = 1
        expected_user_data["is_subscribed"] = False

        self.assertEqual(response_user_data, expected_user_data,
                         f"Проверьте, что в ответе на GET-запрос "
                         f"'{data.USERS_ME_URL}' возвращаются верные данные "
                         f"о пользователе.")

    def test_set_password_with_token(self):
        new_password = "new_awesome_password"
        response = self.client.post(
            data.USERS_SET_PASSWORD_URL,
            data={"new_password": new_password,
                  "current_password": data.USER_DATA_1["password"]}
        )
        self.assertNotEqual(response.status_code,
                            status.HTTP_404_NOT_FOUND,
                            f"Проверьте, что страница "
                            f"'{data.USERS_SET_PASSWORD_URL}' доступна.")
        # self.assertEqual(response.status_code,
        #                  status.HTTP_201_CREATED,
        #                  "Проверьте, что при изменении пароля возвращается "
        #                  "статус 201.")

    def test_set_password_without_token(self):
        new_password = "new_awesome_password"
        self.client.credentials()
        response = self.client.post(
            data.USERS_SET_PASSWORD_URL,
            data={"new_password": new_password,
                  "current_password": data.USER_DATA_1["password"]}
        )
        self.assertEqual(response.status_code,
                            status.HTTP_401_UNAUTHORIZED,
                            f"Проверьте, что страница запрос на"
                            f"'{data.USERS_SET_PASSWORD_URL}' возвращает статус"
                            f" 401.")
        self.authenticate()
