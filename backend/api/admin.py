from django.contrib import admin


from .models import (Ingredient, Recipe, RecipeFavourite, RecipeShoppingCart,
                     RecipeIngredientsDetails, Tag)


class IngredientAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]


class RecipeIngredientsDetailsInline(admin.TabularInline):
    model = RecipeIngredientsDetails
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    search_fields = ["name", "text"]
    list_filter = ["author", "tags"]
    list_display = ["name", "author"]
    inlines = [RecipeIngredientsDetailsInline]


class TagAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "slug"]


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(RecipeFavourite)
admin.site.register(RecipeShoppingCart)
