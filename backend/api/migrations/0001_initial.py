# Generated by Django 3.2.5 on 2021-08-20 14:44

import colorfield.fields
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название ингридиента', max_length=200, verbose_name='Название')),
                ('measurement_unit', models.CharField(help_text='Введите единицу измерения ингредиента', max_length=200, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название рецепта', max_length=200, verbose_name='Название')),
                ('image', models.ImageField(help_text='Загрузите изображение', upload_to='recipes', verbose_name='Изображение')),
                ('text', models.TextField(help_text='Введите текстовое описание', verbose_name='Текстовое описание')),
                ('cooking_time', models.PositiveSmallIntegerField(help_text='Введите время приготовления в минутах', validators=[django.core.validators.MinValueValidator(limit_value=1, message='Время приготовления должно быть не менее 1.')], verbose_name='Время приготовления (мин)')),
                ('pub_date', models.DateTimeField(auto_now=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(help_text='Введите имя автора', on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите тег', max_length=200, unique=True, verbose_name='Название')),
                ('color', colorfield.fields.ColorField(default='#888888', help_text='Выберите цветовой HEX-код (пример: #FF0033)', max_length=200, validators=[django.core.validators.RegexValidator(message='Цвет должен быть задан в формате hex-кода', regex='#[0-9a-fA-F]{6}')], verbose_name='Цвет')),
                ('slug', models.SlugField(help_text='Введите slug', unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredientsDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(help_text='Введите количество', validators=[django.core.validators.MinValueValidator(limit_value=1, message='Количество должно быть не менее 1.')], verbose_name='Количество')),
                ('ingredient', models.ForeignKey(help_text='Выберите ингредиент', on_delete=django.db.models.deletion.CASCADE, to='api.ingredient', verbose_name='Ингредиент')),
                ('recipe', models.ForeignKey(help_text='Выберите рецепт', on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_details', to='api.recipe', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Ингридиент рецепта',
                'verbose_name_plural': 'Ингридиенты рецепта',
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(help_text='Выберите ингридиенты', through='api.RecipeIngredientsDetails', to='api.Ingredient', verbose_name='Ингридиенты'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(help_text='Выберите теги', to='api.Tag', verbose_name='Теги'),
        ),
        migrations.CreateModel(
            name='UserFollow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follow_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL, verbose_name='Подписан на пользователя')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follows', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Подписки на авторов',
                'verbose_name_plural': 'Подписки на авторов',
                'unique_together': {('user', 'follow_to')},
            },
        ),
        migrations.CreateModel(
            name='RecipeShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(help_text='Выберите рецепт', on_delete=django.db.models.deletion.CASCADE, related_name='to_shopping', to='api.recipe', verbose_name='Рецепт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Список покупок',
                'verbose_name_plural': 'Списки покупок',
                'unique_together': {('user', 'recipe')},
            },
        ),
        migrations.CreateModel(
            name='RecipeFavourite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourites', to='api.recipe', verbose_name='Рецепт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_favourites', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранное',
                'unique_together': {('user', 'recipe')},
            },
        ),
    ]
