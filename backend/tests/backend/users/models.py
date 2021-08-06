from django.contrib.auth.models import AbstractUser, UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        verbose_name="Имя пользователя",
        max_length=150,
        unique=True,
        help_text="Введите имя пользователя "
                  "(Только буквы, цифры и символы @/./+/-/_ )",
        validators=[UnicodeUsernameValidator()],
        error_messages={
            "unique": "Пользователь с таким логином уже существует.",
        },
    )
    first_name = models.CharField(
        verbose_name="Имя",
        help_text="Введите имя",
        max_length=150,
        blank=False,
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        help_text="Введите фамилию",
        max_length=150,
        blank=False,
    )
    email = models.EmailField(
        verbose_name="E-mail",
        help_text="Введите адрес электронной почты",
        max_length=254,
        unique=True,
        blank=False,
    )
    REQUIRED_FIELDS = ["password", "email", "first_name", "last_name"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
