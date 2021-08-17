from django.contrib.auth import views as auth_views
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (author_page, favorite_recipes, index, recipe_create,
                    recipe_single, recipes_list, shopping_cart, ingredients_list,
                    AboutPage, SignUp,
                    WebsiteRecipeFavouriteViewSet, WebsiteShoppingCartViewSet,
                    WebsiteSubscriptionsViewSet)


router = DefaultRouter()

urlpatterns = [
    path("", index, name="index"),
    path("signup/", SignUp.as_view(), name="signup"),
    path("login/", auth_views.LoginView.as_view(), name="web-login"),
    path("logout/", auth_views.LogoutView.as_view(), name="web-logout"),

    path("favorite/", favorite_recipes, name="web-favorite-recipes"),
    path("recipes/", recipes_list, name="web-recipes"),
    path("recipes/<int:recipe_id>/", recipe_single, name="web-recipe-single"),
    path("recipes/<int:recipe_id>/favorite/",
         WebsiteRecipeFavouriteViewSet.as_view({
             "get": "create", "delete": "destroy"}),
         name="web-recipes-favorite"),
    path("recipes/<int:recipe_id>/shopping_cart/",
         WebsiteShoppingCartViewSet.as_view(
             {"get": "create", "delete": "destroy"}),
         name="web-recipes-shopping-cart"),
    path('recipes/download_shopping_cart/',
         WebsiteShoppingCartViewSet.as_view({'get': 'list'}),
         name='web-shopping-cart-download'),

    path("recipes/create/", recipe_create, name="web-recipe-create"),

    path("users/<int:author_id>/", author_page, name="web-author-page"),
    path("users/<int:author_id>/subscribe/",
         WebsiteSubscriptionsViewSet.as_view(
             {"get": "create", "delete": "destroy"}),
         name="web-subscribe"),
    path("users/subscriptions/",
         WebsiteSubscriptionsViewSet.as_view({"get": "list"}),
         name="web-subscriptions"),

    path("shopping_cart/", shopping_cart, name="web-shopping-cart"),

    path("ingredients/", ingredients_list, name="web-ingredients"),

    path("about/", AboutPage.as_view(), name="web-about")
]
