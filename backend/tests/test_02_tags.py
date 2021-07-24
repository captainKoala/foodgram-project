from typing import List

from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Tag

from . import data


class TagsTestCase(APITestCase):
    def setUp(self):
        Tag.objects.create(**data.TAG_DATA_1)
        Tag.objects.create(**data.TAG_DATA_2)

    def test_get_tags_list(self):
        response = self.client.get(data.TAGS_LIST_URL)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"Проверьте, что запрос на адрес '{data.TAGS_LIST_URL}' возвращает"
            f" статус 200."
        )
        self.assertEqual(
            len(response.data),
            2,
            f"Проверьте, что в ответе по запросу на адрес "
            f"'{data.TAGS_LIST_URL}' передаются все теги."
        )
        self.assertIsInstance(
            response.data,
            List,
            f"Проверьте, что в ответе по запросу на адрес "
            f"'{data.TAGS_LIST_URL}' передается список."
        )

        expected_data = data.TAG_DATA_1.copy()
        expected_data["id"] = 1
        self.assertEqual(
            response.data[0],
            expected_data,
            f"Проверьте, что в ответе по запросу на адрес "
            f"'{data.TAGS_LIST_URL}' "
            f"каждый тег содержит необходимые поля."
        )

    def test_get_tag_by_id(self):
        tag_id = 1
        url = f"{data.TAGS_LIST_URL}{tag_id}/"
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"Проверьте, что запрос на адрес '{data.TAGS_LIST_URL}{{tag_id}}/'"
            f" возвращает статус 200."
        )
        expected_data = data.TAG_DATA_1.copy()
        expected_data["id"] = 1
        self.assertEqual(
            response.data,
            expected_data,
            f"Проверьте, что в ответе по запросу на адрес "
            f"'{data.TAGS_LIST_URL}{{tag_id}}/' "
            f"каждый тег содержит необходимые поля."
        )
