from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import index, recipe_favourites, IngredientViewSet, RecipeViewSet, TagViewSet

router = DefaultRouter()
router.register('ingredients', IngredientViewSet, basename='ingredientss')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')

urlpatterns = [
    path('recipes/<int:recipe_id>/favorite/',
         recipe_favourites,
         name="recipe_to_favourites"),
    path('', include(router.urls)),
]
