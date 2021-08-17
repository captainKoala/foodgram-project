from django.core.paginator import Paginator
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy

from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

from .forms import CustomUserCreationForm, IngredientsFormSet, RecipeCreateForm
from api.models import Ingredient, Recipe, Tag
from api.views import (RecipeFavouriteViewSet, ShoppingCartViewSet,
                       SubscriptionsViewSet)
from users.models import User


RECIPES_PER_PAGE = 6


def index(request):
    """ Главная страница сайта. """
    if request.user.is_authenticated:
        return redirect(reverse_lazy("web-recipes"))
    return redirect(reverse_lazy("web-login"))


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("signup")
    template_name = "signup.html"


class WebsiteRecipeFavouriteViewSet(RecipeFavouriteViewSet):
    """Добавление и удаление рецепта из избранного."""
    authentication_classes = (SessionAuthentication, )


class WebsiteShoppingCartViewSet(ShoppingCartViewSet):
    """Добавление и удаление рецепта из списка покупок."""
    authentication_classes = (SessionAuthentication, )


def create_context(request):
    """Извлечение параметров из запроса и формирование контекста для ответа."""
    selected_tags = request.GET.getlist("tags")

    tags = Tag.objects.all()
    if not selected_tags:
        selected_tags = tuple(tag.slug for tag in tags)

    shopping_cart = favorite = 0
    if request.user.is_authenticated:
        shopping_cart = Recipe.objects.filter(to_shopping__user=request.user)
        favorite = Recipe.objects.filter(favourites__user=request.user)

    return {
        "favorite_recipes": favorite,
        "selected_tags": selected_tags,
        "shopping_cart": shopping_cart,
        "tags": tags,
    }


class WebsiteSubscriptionsViewSet(SubscriptionsViewSet):
    """Добавление и удаление подписки на автора."""
    authentication_classes = (SessionAuthentication, )
    renderer_classes = (JSONRenderer, TemplateHTMLRenderer, )
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect(reverse_lazy("web-login"))
        response = super().list(request, *args, **kwargs)

        context = create_context(request)

        context["authors"] = response.data.get("results")
        return Response(context,
                        template_name="subscriptions.html")


def recipe_single(request, recipe_id):
    """Страница с одним рецептом."""
    context = create_context(request)
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user.is_anonymous:
        is_followed = False
    else:
        is_followed = recipe.author.followers.filter(user=request.user).exists()

    context["recipe"] = recipe
    context["is_followed"] = is_followed
    return render(request, context=context, template_name="recipe-single.html")


def recipes_list(request):
    """Страница со списком рецептов."""
    context = create_context(request)

    recipes = (Recipe.objects.none()
               if "__none__" in context["selected_tags"] else
               Recipe.objects.filter(tags__slug__in=context["selected_tags"])
               .distinct().order_by("-pub_date"))

    paginator = Paginator(recipes, RECIPES_PER_PAGE)
    page_number = request.GET.get("page")
    context["recipes"] = paginator.get_page(page_number)
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


def recipe_create(request):
    """Создание нового рецепта."""
    if request.user.is_anonymous:
        return redirect(reverse_lazy("web-login"))

    prefix = "ingredient"

    if request.method == "POST":
        from pprint import pprint
        pprint(request.POST)
        form = RecipeCreateForm(data=request.POST, files=request.FILES)
        formset = IngredientsFormSet(data=request.POST, prefix=prefix)
        if form.is_valid() and formset.is_valid():
            recipe = form.save(commit=False)
            recipe.author_id = request.user.id
            recipe.save()
            form.save_m2m()
            formset.instance = recipe
            formset.save()
            return redirect(reverse_lazy("index"))
        context = {"form": form, "formset": formset}
        return render(request, template_name="recipe-create.html",
                      context=context)

    form = RecipeCreateForm()
    formset = IngredientsFormSet({f"{prefix}-INITIAL_FORMS": "0",
                                  f"{prefix}-MAX_NUM_FORMS": "5",
                                  f"{prefix}-MIN_NUM_FORMS": "1",
                                  f"{prefix}-TOTAL_FORMS": "2", },
                                 prefix=prefix,)
    context = {"form": form, "formset": formset, }
    return render(request, context=context, template_name="recipe-create.html")


def author_page(request, author_id):
    """Страница автора рецепта."""
    context = create_context(request)

    author = get_object_or_404(User, id=author_id)
    recipes = (Recipe.objects.none()
               if "__none__" in context["selected_tags"] else
               author.recipes.filter(tags__slug__in=context["selected_tags"])
               .distinct().order_by("-pub_date"))

    if request.user.is_anonymous:
        is_followed = False
    else:
        is_followed = author.followers.filter(user=request.user).exists()

    paginator = Paginator(recipes, RECIPES_PER_PAGE)
    page_number = request.GET.get("page")
    context["recipes"] = paginator.get_page(page_number)
    context["author"] = author
    context["is_followed"] = is_followed
    return render(request, context=context, template_name="author.html")


def shopping_cart(request):
    """Страница рецептов, добавленных в список покупок."""
    recipes = Recipe.objects.filter(to_shopping__user=request.user)
    context = create_context(request)
    context["recipes"] = recipes
    return render(request, context=context, template_name="shopping-cart.html")


from api.views import ShoppingCartViewSet

class WebShoppingCartViewSet(ShoppingCartViewSet):
    authentication_classes = (SessionAuthentication, )


class AboutPage(TemplateView):
    template_name = "about.html"


def ingredients_list(request):
    if request.is_ajax():
        term = request.GET.get("term")
        heroes = Ingredient.objects.filter(name__icontains=term)
        response_content = list(heroes.values())
        return JsonResponse(response_content, safe=False)
    return redirect("index")
