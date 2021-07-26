from django.contrib import admin

from .models import (Ingredient, Recipe, RecipeFavourite,
                     RecipeIngredientsDetails, RecipeShoppingCart, Tag)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_display = ("name",)
    list_filter = ("name",)


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
    list_display = ("user", "recipe")


@admin.register(RecipeShoppingCart)
class RecipeShoppingCartAdmin(admin.ModelAdmin):
    list_display = ("user", "recipe")
