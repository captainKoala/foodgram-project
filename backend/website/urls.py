from django.contrib.auth import views as auth_views
from django.urls import path

from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(), name="web-login"),
    path("logout/", auth_views.LogoutView.as_view(), name="web-logout"),
    path("password-reset/", views.CustomPasswordResetView.as_view(),
         name="web-password-reset"),
    path("password-reset/done", views.CustomPasswordResetDoneView.as_view(),
         name="password_reset_done"),
    path("reset/<uidb64>/<token>/",
         views.CustomPasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path("reset/done/", views.CustomPasswordResetCompleteView.as_view(),
         name="password_reset_complete"),
    path("activate/<uid>/<token>/", views.ActivateUser.as_view(),
         name="web-account-activation"),
    path("password-change/", views.CustomPasswordChangeView.as_view(),
         name="password_change"),

    path("password-change/done/", views.CustomPasswordChangeDoneView.as_view(),
         name="password_change_done"),

    path("favorite/", views.favorite_recipes, name="web-favorite-recipes"),
    path("recipes/", views.recipes_list, name="web-recipes"),
    path("recipes/<int:recipe_id>/", views.recipe_single, name="web-recipe-single"),
    path("recipes/create/", views.recipe_edit, name="web-recipe-create"),
    path("recipes/<int:recipe_id>/edit/", views.recipe_edit, name="web-recipe-edit"),
    path("recipes/<int:recipe_id>/remove/", views.recipe_remove,
         name="web-recipe-remove"),
    path("recipes/<int:recipe_id>/favorite/",
         views.WebsiteRecipeFavouriteViewSet.as_view({
             "get": "create", "delete": "destroy"}),
         name="web-recipes-favorite"),
    path("recipes/<int:recipe_id>/shopping_cart/",
         views.WebsiteShoppingCartViewSet.as_view(
             {"get": "create", "delete": "destroy"}),
         name="web-recipes-shopping-cart"),
    path('recipes/download_shopping_cart/',
         views.WebsiteShoppingCartViewSet.as_view({'get': 'list'}),
         name='web-shopping-cart-download'),


    path("users/<int:author_id>/", views.author_page, name="web-author-page"),
    path("users/<int:author_id>/subscribe/",
         views.WebsiteSubscriptionsViewSet.as_view(
             {"get": "create", "delete": "destroy"}),
         name="web-subscribe"),
    path("users/subscriptions/",
         views.WebsiteSubscriptionsViewSet.as_view({"get": "list"}),
         name="web-subscriptions"),

    path("shopping_cart/", views.shopping_cart, name="web-shopping-cart"),
    path("shopping_cart/remove/<int:recipe_id>/",
         views.shopping_cart_remove,
         name="web-remove-from-shopping-cart"),

    path("ingredients/", views.ingredients_list, name="web-ingredients"),

    path("about/", views.AboutPage.as_view(), name="web-about")
]
