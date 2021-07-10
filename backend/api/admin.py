from django.contrib import admin


from .models import Ingredient, Recipe, RecipeIngredients, Tag


class IngredientAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]


class RecipeAdmin(admin.ModelAdmin):
    search_fields = ["name", "text"]
    list_filter = ["author", "tags"]
    list_display = ["name", "author"]


class TagAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "slug"]


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)

admin.site.register(RecipeIngredients)
