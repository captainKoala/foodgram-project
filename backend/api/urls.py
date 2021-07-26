from django.urls import include, path
from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, RecipeViewSet, SubscriptionsViewSet,
                    TagViewSet, get_shopping_cart, manage_shopping_cart,
                    recipe_favourites, subscribe)

api_router = DefaultRouter()
api_router.register('ingredients', IngredientViewSet, basename='ingredients')
api_router.register('recipes', RecipeViewSet, basename='recipes')
api_router.register('tags', TagViewSet, basename='tags')

from .views import index

urlpatterns = [
    path('temp/', index),
    path('api/recipes/<int:recipe_id>/favorite/',
         recipe_favourites,
         name='manage_recipe_favourites'),
    path('api/recipes/download_shopping_cart/',
         get_shopping_cart,
         name='get_shopping_cart'),
    path('api/recipes/<int:recipe_id>/shopping_cart/',
         manage_shopping_cart,
         name='manage_shopping_cart'),
    path('api/', include(api_router.urls)),
    path('api/users/subscriptions/',
         SubscriptionsViewSet.as_view({'get': 'list'}),
         name='subscriptions'),
    path('api/users/<int:author_id>/subscribe/',
         subscribe,
         name='subscribe'),
]
