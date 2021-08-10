from django.contrib.auth import views
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (author_page, favorite_recipes, index, recipe_single, recipes_list, signup,
                    WebsiteRecipeFavouriteViewSet, WebsiteShoppingCartViewSet,
                    WebsiteSubscriptionsViewSet)


router = DefaultRouter()

urlpatterns = [
    path("", index, name="index"),
    path("signup/", signup, name="signup"),
    path("login/", views.LoginView.as_view(), name="web-login"),
    path("logout/", views.LogoutView.as_view(), name="web-logout"),
    path("favorite/", favorite_recipes, name="web-favorite-recipes"),
    path("recipes/", recipes_list, name="web-recipes"),
    path("recipes/<int:recipe_id>/", recipe_single, name="web-recipe-single"),
    path('recipes/<int:recipe_id>/favorite/',
         WebsiteRecipeFavouriteViewSet.as_view({'get': 'create',
                                                'delete': 'destroy'}),
         name='web_recipes_favorite'),
    path('recipes/<int:recipe_id>/shopping_cart/',
         WebsiteShoppingCartViewSet.as_view({'get': 'create',
                                             'delete': 'destroy'}),
         name='web_recipes_shopping_cart'),
    path("users/<int:author_id>/", author_page, name="web-author-page"),
    path('users/<int:author_id>/subscribe/',
         WebsiteSubscriptionsViewSet.as_view({'get': 'create',
                                              'delete': 'destroy'}),
         name='web_recipes_shopping_cart'),
]
