from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name="Название",
        help_text="Введите название ингридиента",
        max_length=200,
    )
    measurement_unit = models.CharField(
        verbose_name="Единица измерения",
        help_text="Введите единицу измерения",
        max_length=200,
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        verbose_name="Название",
        help_text="Введите тег",
        max_length=200,
        unique=True,
    )
    color = models.CharField(
        verbose_name="Цвет",
        help_text="Выберите цветовой HEX-код (пример: #FF0033)",
        max_length=200,
        unique=True,
        validators=[RegexValidator(regex=r"#[0-9a-fA-F]{6}")],
    )
    slug = models.SlugField(
        verbose_name="Slug",
        help_text="Введите slug",
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name="Ингредиент",
        help_text="Добавьте ингредиент",
        on_delete=models.CASCADE,
    )
    amount = models.FloatField(
        verbose_name="Количество",
        help_text="Введите количество"
    )


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        help_text="Введите имя автора",
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name="Название",
        help_text="Введите название рецепта",
        max_length=200,
    )
    image = models.ImageField(
        verbose_name="Изображение",
        help_text="Добавьте изображение",
    )
    text = models.TextField(
        verbose_name="Текстовое описание",
        help_text="Введите текстовое описание",
    )
    ingredients = models.ManyToManyField(
        RecipeIngredients,
        verbose_name="Ингридиенты",
        help_text="Выберите ингридиенты",
        related_name="Рецепты",
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Теги",
        help_text="Выберите теги",
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name="Время приготовления (мин)",
        help_text="Введите время приготовления в минутах",
        validators=[MinValueValidator(limit_value=1)]
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name[:30]
