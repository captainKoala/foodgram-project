from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from rest_framework.authentication import SessionAuthentication

from api.models import Recipe, Tag
from api.views import (RecipeFavouriteViewSet, ShoppingCartViewSet,
                       SubscriptionsViewSet)
from users.models import User


def index(request):
    """ Главная страница сайта. """
    if request.user.is_authenticated:
        return redirect(reverse("web-recipes"))
    return redirect(reverse("web-login"))


def signup(request):
    """Страница регистрации пользователя."""
    if request.method == "POST":
        pass
    return render(request, "signup.html", context=context)


class WebsiteRecipeFavouriteViewSet(RecipeFavouriteViewSet):
    """Добавление и удаление рецепта из избранного."""
    authentication_classes = (SessionAuthentication, )


class WebsiteShoppingCartViewSet(ShoppingCartViewSet):
    """Добавление и удаление рецепта из списка покупок."""
    authentication_classes = (SessionAuthentication, )


class WebsiteSubscriptionsViewSet(SubscriptionsViewSet):
    """Добавление и удаление подписки на автора."""
    authentication_classes = (SessionAuthentication, )


def create_context(request):
    """Извлечение параметров из запроса и формирование контекста для ответа."""
    selected_tags = request.GET.getlist("tags")

    tags = Tag.objects.all()
    if not selected_tags:
        selected_tags = tuple(tag.slug for tag in tags)

    if request.user.is_authenticated:
        shopping_cart = Recipe.objects.filter(to_shopping__user=request.user)
        favorite_recipes = Recipe.objects.filter(favourites__user=request.user)
    else:
        shopping_cart = favorite_recipes = 0
    return {
        "favorite_recipes": favorite_recipes,
        "selected_tags": selected_tags,
        "shopping_cart": shopping_cart,
        "tags": tags,
    }


def recipe_single(request, recipe_id):
    """Страница с одним рецептом."""
    context = create_context(request)
    recipe = get_object_or_404(Recipe, id=recipe_id)
    context["recipe"] = recipe
    return render(request, context=context, template_name="recipe-single.html")


def recipes_list(request):
    """Страница со списком рецептов."""
    context = create_context(request)

    recipes = (Recipe.objects.none()
               if "__none__" in context["selected_tags"] else
               Recipe.objects.filter(tags__slug__in=context["selected_tags"])
               .distinct().order_by("-pub_date"))

    context["recipes"] = recipes
    return render(request, context=context, template_name="recipes.html")


def favorite_recipes(request):
    """Страница с избранными рецептами."""
    context = create_context(request)

    recipes = (Recipe.objects.none()
               if "__none__" in context["selected_tags"] else
               context["favorite_recipes"].filter(tags__slug__in=context["selected_tags"])
               .distinct().order_by("-pub_date"))

    context["recipes"] = recipes
    return render(request, context=context, template_name="recipes.html")


def author_page(request, author_id):
    """Страница автора рецепта."""
    context = create_context(request)

    author = get_object_or_404(User, id=author_id)
    recipes = (Recipe.objects.none()
               if "__none__" in context["selected_tags"] else
               author.recipes.filter(tags__slug__in=context["selected_tags"])
               .distinct().order_by("-pub_date"))
    is_followed = author in request.user.follows.all()

    context["author"] = author
    context["recipes"] = recipes
    context["is_followed"] = is_followed
    return render(request, context=context, template_name="author.html")
