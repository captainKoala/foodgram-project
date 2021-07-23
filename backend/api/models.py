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
        return f"{self.name} ({self.measurement_unit})"


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


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        help_text="Введите имя автора",
        on_delete=models.CASCADE,
        related_name="recipes",
    )
    name = models.CharField(
        verbose_name="Название",
        help_text="Введите название рецепта",
        max_length=200,
    )
    image = models.ImageField(
        verbose_name="Изображение",
        help_text="Загрузите изображение",
        upload_to="recipes",
        null=True,
        blank=True,
    )
    text = models.TextField(
        verbose_name="Текстовое описание",
        help_text="Введите текстовое описание",
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name="Ингридиенты",
        help_text="Выберите ингридиенты",
        through='RecipeIngredientsDetails',
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
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now=True,
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name[:30]


class RecipeIngredientsDetails(models.Model):
    """ Описывает количество для каждого ингридиента в рецепте."""
    recipe = models.ForeignKey(
        Recipe,
        verbose_name="Рецепт",
        help_text="Выберите рецепт",
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name="Ингредиент",
        help_text="Добавьте ингредиент",
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField(
        verbose_name="Количество",
        help_text="Введите количество",
        validators=[MinValueValidator(limit_value=1)],
    )

    class Meta:
        verbose_name = "Ингридиент рецепта"
        verbose_name_plural = "Ингридиенты рецепта"

    def __str__(self):
        return f"{self.recipe} - {self.ingredient}"


class RecipeFavourite(models.Model):
    """ Добавление рецепта в избранное. """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="recipe_favourites",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
        related_name="favourites",
    )

    class Meta:
        unique_together = [['user', 'recipe']]
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"

    def __str__(self):
        return f"{self.user} - {self.recipe}"


class RecipeShoppingCart(models.Model):
    """ Добавление рецепта в список покупок. """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name="Рецепт",
        help_text="Выберите рецепт",
        on_delete=models.CASCADE,
        related_name="to_shopping",
    )

    class Meta:
        unique_together = [['user', 'recipe']]
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"

    def __str__(self):
        return f"{self.user} - {self.recipe}"


class UserFollow(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name="follows",
    )
    follow_to = models.ForeignKey(
        User,
        verbose_name="Подписан на пользователя",
        on_delete=models.CASCADE,
        related_name="followers",
    )

    class Meta:
        unique_together = [["user", "follow_to"]]
