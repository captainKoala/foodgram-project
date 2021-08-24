import requests
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response

from api.models import Ingredient, Recipe, RecipeIngredientsDetails, Tag
from api.views import (RecipeFavouriteViewSet, ShoppingCartViewSet,
                       SubscriptionsViewSet)
from users.models import User

from .forms import CustomUserCreationForm, IngredientsFormSet, RecipeCreateForm

RECIPES_PER_PAGE = 6
INGREDIENT_FORMSET_PREFIX = "ingredient"


def index(request):
    """ Главная страница сайта. """
    if request.user.is_authenticated:
        return redirect(reverse_lazy("web-recipes"))
    return redirect(reverse_lazy("web-login"))


def signup(request):
    """ Страница регистрации пользователя. """
    if request.user.is_authenticated:
        return redirect(reverse_lazy("index"))
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            url = settings.PROTOCOL + settings.DOMAIN + "/api/users/"
            data = {"username": form.data["username"],
                    "first_name": form.data["first_name"],
                    "last_name": form.data["last_name"],
                    "email": form.data["email"],
                    "password": form.data["password1"]}
            try:
                response = requests.post(url, data=data)
                if response.status_code == 201:
                    return render(
                        request,
                        template_name="registration/signup_success.html")
                if response.status_code == 400:
                    for key, value in response.json().items():
                        if key in form.fields:
                            form.add_error(key, value)
                    return render(request, template_name="signup.html",
                                  context={"form": form})
                error = str(response.status_code) + ": " + response.text
            except requests.exceptions.ConnectionError as e:
                error = e
            except Exception as e:
                error = e
            return render(request,
                          template_name="registration/signup_error.html",
                          context={"response": error})
        return render(request, template_name="signup.html",
                      context={"form": form})
    form = CustomUserCreationForm()
    return render(request, template_name="signup.html",
                  context={"form": form})


class ActivateUser(GenericAPIView):
    """Активация пользователя по ссылке в e-mail."""
    def get(self, request, uid, token):
        payload = {'uid': uid, 'token': token}

        url = settings.PROTOCOL + settings.DOMAIN + "/api/users/activation/"
        response = requests.post(url, data=payload)

        if response.status_code == 204:
            return render(
                request,
                template_name="register/email_confirm_success.html")
        try:
            error = response.json().get("detail")
        except:
            error = "Неизвестная ошибка"
        return render(request, context={"error": error},
                      template_name="register/email_confirm_error.html")


class CustomPasswordChangeView(auth_views.PasswordChangeView):
    """Смена пароля."""
    template_name = "register/password_change_form.html"


class CustomPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    """Смена пароля успешна"""
    template_name = "register/password_change_done.html"


class CustomPasswordResetView(auth_views.PasswordResetView):
    """Сброс пароля."""
    template_name = "register/password_reset_form.html"


class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    """Сброс пароля успешен."""
    template_name = "register/password_reset_done.html"


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """Форма ввода нового пароля после сброса."""
    template_name = "register/password_reset_confirm.html"


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    """Успешный сброс пароля."""
    template_name = "register/password_reset_complete.html"


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
        is_followed = (recipe.author.followers
                       .filter(user=request.user).exists())

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
    context["title"] = "Рецепты"
    return render(request, context=context, template_name="recipes.html")


@login_required(login_url=reverse_lazy("web-login"))
def favorite_recipes(request):
    """Страница с избранными рецептами."""
    context = create_context(request)

    recipes = (Recipe.objects.none()
               if "__none__" in context["selected_tags"] else
               context["favorite_recipes"]
               .filter(tags__slug__in=context["selected_tags"])
               .distinct().order_by("-pub_date"))

    paginator = Paginator(recipes, RECIPES_PER_PAGE)
    page_number = request.GET.get("page")
    context["recipes"] = paginator.get_page(page_number)
    context["title"] = "Избранное"
    return render(request, context=context, template_name="recipes.html")


@login_required(login_url=reverse_lazy("web-login"))
def recipe_edit(request, recipe_id=None):
    """Страница создания и редактирования рецепта."""
    if recipe_id:
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if (request.user != recipe.author and
                not request.user.groups.filter(
                    name="Администраторы").exists()):
            return redirect(reverse_lazy("web-recipe-single",
                                         kwargs={"recipe_id": recipe_id}))
        title = "Изменение рецепта"
        button_text = "Сохранить изменения"
    else:
        recipe = Recipe()
        title = "Новый рецепт"
        button_text = "Создать рецепт"

    if request.method == "POST":
        data = request.POST.copy()
        data[f"{INGREDIENT_FORMSET_PREFIX}-INITIAL_FORMS"] = 0

        form = RecipeCreateForm(data=data,
                                files=request.FILES,
                                instance=recipe)
        formset = IngredientsFormSet(data=data,
                                     prefix=INGREDIENT_FORMSET_PREFIX,
                                     instance=recipe)
        if form.is_valid() and formset.is_valid():
            recipe = form.save(commit=False)
            recipe.author_id = request.user.id
            recipe.save()
            form.save_m2m()
            (RecipeIngredientsDetails.objects
             .filter(recipe_id=recipe_id).delete())
            formset.instance = recipe
            formset.save()
            return redirect(reverse_lazy("web-recipe-single",
                                         kwargs={"recipe_id": recipe.id}))
        context = {"form": form, "formset": formset, "title": title,
                   "button_text": button_text, }
        return render(request, template_name="recipe-create.html",
                      context=context)

    form = RecipeCreateForm(instance=recipe)

    formset = IngredientsFormSet(
        instance=recipe,
        prefix=INGREDIENT_FORMSET_PREFIX,
    )

    context = {
        "form": form,
        "formset": formset,
        "title": title,
        "button_text": button_text,
    }

    return render(request, context=context, template_name="recipe-create.html")


@login_required(login_url=reverse_lazy("web-login"))
def recipe_remove(request, recipe_id):
    """Удаление рецепта."""
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if (request.user != recipe.author and
            not (request.user.groups.filter(name="Администраторы").exists())):
        return redirect(reverse_lazy("web-recipe-single",
                                     kwargs={"recipe_id": recipe_id}))
    recipe.delete()
    return redirect(reverse_lazy("index"))


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


@login_required(login_url=reverse_lazy("web-login"))
def shopping_cart(request):
    """Страница рецептов, добавленных в список покупок."""
    recipes = Recipe.objects.filter(to_shopping__user=request.user)
    context = create_context(request)
    cart = ShoppingCartViewSet()
    context["purchases"] = cart.get_purchases(request)
    context["recipes"] = recipes
    return render(request, context=context, template_name="shopping-cart.html")


@login_required(login_url=reverse_lazy("web-login"))
def shopping_cart_remove(request, recipe_id):
    """Удаление рецепта из списка покупок и обновление списка ингредиентов."""
    from api.models import RecipeShoppingCart

    cart_recipe = get_object_or_404(RecipeShoppingCart,
                                    recipe_id=recipe_id,
                                    user=request.user)
    cart_recipe.delete()
    return redirect(reverse_lazy("web-shopping-cart"))


class WebShoppingCartViewSet(ShoppingCartViewSet):
    """Добавление и удаление рецепта из списка покупок."""
    authentication_classes = (SessionAuthentication, )


def ingredients_list(request):
    """Список всех ингредиентов."""
    if request.is_ajax():
        term = request.GET.get("term")
        ingredients = Ingredient.objects.filter(name__icontains=term)
        response_content = list(ingredients.values())
        return JsonResponse(response_content, safe=False)
    return JsonResponse([], safe=False)


class AboutPage(TemplateView):
    template_name = "about.html"
