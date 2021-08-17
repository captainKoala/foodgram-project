from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, RecipeViewSet, SubscriptionsViewSet,
                    TagViewSet, RecipeFavouriteViewSet, ShoppingCartViewSet)

api_v1_router = DefaultRouter()
api_v1_router.register('ingredients', IngredientViewSet,
                       basename='ingredients')
api_v1_router.register('recipes', RecipeViewSet, basename='recipes')
api_v1_router.register('tags', TagViewSet, basename='tags')


urlpatterns = [
    path('api/recipes/<int:recipe_id>/favorite/',
         RecipeFavouriteViewSet.as_view({'get': 'create',
                                         'delete': 'destroy'}),
         name='recipe_favorite_detail'),
    path('api/recipes/<int:recipe_id>/shopping_cart/',
         ShoppingCartViewSet.as_view({'get': 'create',
                                      'delete': 'destroy'}),
         name='shopping_cart_detail'),
    path('api/recipes/download_shopping_cart/',
         ShoppingCartViewSet.as_view({'get': 'list'}),
         name='shopping_cart_list'),
    path('api/', include(api_v1_router.urls), name='api_v1'),
    path('api/users/subscriptions/',
         SubscriptionsViewSet.as_view({'get': 'list'}),
         name='subscriptions'),
    path('api/users/<int:author_id>/subscribe/',
         SubscriptionsViewSet.as_view({'get': 'create',
                                       'delete': 'destroy'}),
         name='subscribe'),
]
