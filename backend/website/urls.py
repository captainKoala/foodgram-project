from django.contrib.auth import views
from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (index, signup, WebsiteRecipeViewSet,
                    WebsiteRecipeFavouriteViewSet, WebsiteShoppingCartViewSet)


router = DefaultRouter()

router.register("recipes", WebsiteRecipeViewSet, basename="web-recipes")

urlpatterns = [
    path("", index, name="index"),
    path("signup/", signup, name="signup"),
    path("login/", views.LoginView.as_view(), name="web-login"),
    path("logout/", views.LogoutView.as_view(), name="web-logout"),
    path('recipes/<int:recipe_id>/favorite/',
         WebsiteRecipeFavouriteViewSet.as_view({'get': 'create',
                                                'delete': 'destroy'}),
         name='web_recipes_favorite'),
    path('recipes/<int:recipe_id>/shopping_cart/',
         WebsiteShoppingCartViewSet.as_view({'get': 'create',
                                             'delete': 'destroy'}),
         name='web_recipes_shopping_cart'),
    path("", include(router.urls), name="api_v1"),
]
