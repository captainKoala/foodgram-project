from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from users.models import User

USERS_URL = "/api/users/"
USERS_ME_URL = USERS_URL + "me/"
USERS_SET_PASSWORD_URL = USERS_URL + "set_password/"


USER_DATA_1 = {
            "username": "test_user_1",
            "first_name": "Test",
            "last_name": "User",
            "email": "test_user@ex.com",
            "password": "passwordPhrase_1234",
}
USER_DATA_2 = {
            "username": "test_user_2",
            "first_name": "Second",
            "last_name": "User",
            "email": "test_user_2@ex.com",
            "password": "very_strong_Password_1234",
}


class UserCreateTestCase(APITestCase):
    def test_create_user(self):
        # ПРОВЕРКА СОЗДАНИЯ ПОЛЬЗОВАТЕЛЯ
        data = USER_DATA_1
        response = self.client.post(USERS_URL, data, format="json")
        self.assertNotEqual(response.status_code,
                            status.HTTP_404_NOT_FOUND,
                            f"Проверьте, что адрес {USERS_URL} доступен."
                            )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            "Не удалось создать пользователя с корректными данными"
        )

        # ПРОВЕРКА СОЗДАНИЯ ПОЛЬЗОВАТЕЛЯ С УЖЕ СУЩЕСТВУЮЩИМ ИМЕНЕМ ПОЛЬЗОВАТЕЛЯ
        # ИЛИ E-MAIL
        data2 = data.copy()
        data2["username"] = "another_user"
        response = self.client.post(USERS_URL, data2)
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST,
                         "Проверьте, что невозможно создать двух пользотелей "
                         "с одинаковым username.")
        data2 = data.copy()
        data2["email"] = "another_user@example.com"
        response = self.client.post(USERS_URL, data2)
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST,
                         "Проверьте, что невозможно создать двух пользотелей "
                         "с одинаковым email.")

        # ПРОВЕРКА СОЗДАНИЯ ПОЛЬЗОВАТЕЛЕЙ С НЕПОЛНЫМИ ДАННЫМИ
        fields = data.keys()
        for field in fields:
            incomplete_data = data.copy()
            incomplete_data.pop(field)
            response = self.client.post(USERS_URL, data, format="json")
            self.assertEqual(response.status_code,
                             status.HTTP_400_BAD_REQUEST,
                             f"Поле '{field}' обязательно для создания"
                             f"пользователя."
                             )


class UserTestCase(APITestCase):
    def setUp(self):
        self.user_1 = User.objects.create(**USER_DATA_1)
        self.user_2 = User.objects.create(**USER_DATA_2)
        self.token_1 = Token.objects.create(user=self.user_1)
        self.authenticate()

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_1}")

    def test_get_users_list(self):
        response = self.client.get(USERS_URL)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK,
                         f"Проверьте, что список пользователей доступен "
                         f"по адресу '{USERS_URL}' для "
                         f"авторизованного пользователя.")

        response_count = response.data.get("count")
        response_user_1_data = response.data.get("results")[0]

        # По ReDOC ожидаются поля email, id, username,
        # first_name, last_name, is_subscribed
        expected_user_data = USER_DATA_1.copy()
        expected_user_data.pop("password")
        expected_user_data["id"] = 1
        expected_user_data["is_subscribed"] = False
        self.assertEqual(response_count, User.objects.all().count(),
                         f"Проверьте, что в ответе на GET-запрос "
                         f"'{USERS_URL}' возвращается верное количество "
                         f"пользователей.")
        self.assertEqual(response_user_1_data, expected_user_data,
                         f"Проверьте, что в ответе на GET-запрос "
                         f"'{USERS_URL}' возвращаются верные данные о "
                         f"пользователе.")

    def test_get_user_by_id_with_token(self):
        user_id = 2
        url = f"{USERS_URL}{user_id}/"

        response = self.client.get(url)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK,
                         f"Проверьте, что авторизованному пользователю "
                         f"доступна страница '{USERS_URL}{{id}}'."
                         )

        response_user_data = response.data
        expected_user_data = USER_DATA_2.copy()
        expected_user_data.pop("password")
        expected_user_data["id"] = user_id
        expected_user_data["is_subscribed"] = False

        self.assertEqual(response_user_data, expected_user_data,
                         f"Проверьте, что в ответе на GET-запрос "
                         f"'{USERS_URL}{{id}}' возвращаются верные данные "
                         f"о пользователе.")

    def test_get_user_by_id_without_token(self):
        user_id = 2
        url = f"{USERS_URL}{user_id}/"

        self.client.credentials()
        response = self.client.get(url)
        # В ReDoc описан код 403 для неавторизованного пользователя,
        # но это видится неправильным
        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED,
                         f"Проверьте, что неавторизованному пользователю "
                         f"недоступна страница '{USERS_URL}{{id}}'."
                         )
        self.authenticate()

    def test_get_current_user_with_token(self):
        response = self.client.get(USERS_ME_URL)
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK,
                         f"Проверьте, что авторизованному пользователю "
                         f"доступна страница '{USERS_ME_URL}'."
                         )

        response_user_data = response.data
        expected_user_data = USER_DATA_1.copy()
        expected_user_data.pop("password")
        expected_user_data["id"] = 1
        expected_user_data["is_subscribed"] = False

        self.assertEqual(response_user_data, expected_user_data,
                         f"Проверьте, что в ответе на GET-запрос "
                         f"'{USERS_ME_URL}' возвращаются верные данные "
                         f"о пользователе.")

    def test_set_password_with_token(self):
        new_password = "new_awesome_password"
        response = self.client.post(
            USERS_SET_PASSWORD_URL,
            data={"new_password": new_password,
                  "current_password": USER_DATA_1["password"]}
        )
        self.assertNotEqual(response.status_code,
                            status.HTTP_404_NOT_FOUND,
                            f"Проверьте, что страница "
                            f"'{USERS_SET_PASSWORD_URL}' доступна.")
        # self.assertEqual(response.status_code,
        #                  status.HTTP_201_CREATED,
        #                  "Проверьте, что при изменении пароля возвращается "
        #                  "статус 201.")

    def test_set_password_without_token(self):
        new_password = "new_awesome_password"
        self.client.credentials()
        response = self.client.post(
            USERS_SET_PASSWORD_URL,
            data={"new_password": new_password,
                  "current_password": USER_DATA_1["password"]}
        )
        self.assertEqual(response.status_code,
                            status.HTTP_401_UNAUTHORIZED,
                            f"Проверьте, что страница запрос на"
                            f"'{USERS_SET_PASSWORD_URL}' возвращает статус"
                            f" 401.")
        self.authenticate()
