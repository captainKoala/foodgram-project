from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (recipe_favourites, list_recipe_favourites, get_shopping_cart,
                    manage_shopping_cart, IngredientViewSet, RecipeViewSet,
                    RecipeIngredientDetailsViewSet, TagViewSet)

router = DefaultRouter()
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')

urlpatterns = [
    path('api/recipes/<int:recipe_id>/favorite/',
         recipe_favourites,
         name='manage_recipe_favourites'),
    path('api/recipes/download_shopping_cart/',
         get_shopping_cart,
         name='get_shopping_cart'),
    path('api/recipes/<int:recipe_id>/shopping_cart/',
         manage_shopping_cart,
         name='manage_shopping_cart'),
    path('api/', include(router.urls)),
]
