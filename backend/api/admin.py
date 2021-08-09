from django.contrib import admin
from django_select2 import forms as s2forms

from .models import (Ingredient, Recipe, RecipeFavourite,
                     RecipeIngredientsDetails, RecipeShoppingCart, Tag)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name",)
    list_filter = ("name",)


class IngredientWidget(s2forms.ModelSelect2Widget):
    search_fields = ["name__icontains"]
    queryset = Ingredient.objects.all()

    class Media:
        js = ("admin/js/vendor/jquery/jquery.min.js",)


class RecipeIngredientsDetailsInline(admin.TabularInline):
    model = RecipeIngredientsDetails
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    search_fields = ("name", "text")
    list_filter = ("author", "name", "tags")
    list_display = ("name", "author")
    inlines = [RecipeIngredientsDetailsInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name", "slug")


@admin.register(RecipeFavourite)
class RecipeFavouriteAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe", )
    list_filter = ("user",)


@admin.register(RecipeShoppingCart)
class RecipeShoppingCartAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")
    list_filter = ("user",)
