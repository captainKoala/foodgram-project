from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.urls import reverse

from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from api.models import Recipe, Tag
from api.views import RecipeViewSet, RecipeFavouriteViewSet, ShoppingCartViewSet, TagViewSet
from .forms import CreationForm


def index(request):
    """ Главная страница сайта. """
    if request.user.is_authenticated:
        return redirect(reverse("web-recipes-list"))
    return redirect(reverse("web-login"))


def signup(request):
    """Страница регистрации пользователя."""
    if request.method == "POST":
        print("\n"*5)
        url = "http://" + str(get_current_site(request)) + reverse("user-list")
        print(url)

        request_data = request.POST
        data = {}
        data["username"] = request_data["username"]
        data["first_name"] = request_data["first_name"]
        data["last_name"] = request_data["last_name"]
        data["email"] = request_data["email"]
        # data["password"] = request_data["password"]

        print(data)
        # headers = {
        #     'Content-Type': 'application/json'
        # }
        # response = requests.request("POST", url, headers=headers, data=data)
        # print(response.json())

    form = CreationForm()
    context = {
        "form": form,
    }
    return render(request, "signup.html", context=context)


class WebsiteRecipeViewSet(RecipeViewSet):
    """Управление рецептами"""
    renderer_classes = (TemplateHTMLRenderer,)
    authentication_classes = (SessionAuthentication, )

    def retrieve(self, request, *args, **kwargs):
        # instance = self.get_object()
        # serializer = self.get_serializer(instance)
        # return Response(serializer.data)
        response = super().retrieve(self, request, *args, **kwargs)
        recipe = response.data
        context = {"recipe": recipe}
        return Response(context, template_name="recipe-single.html")

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        selected_tags = request.query_params.getlist("tags")
        is_favorited = request.query_params.get("is_favorited")

        title = "Избранное" if is_favorited else "Рецепты"

        if not selected_tags:
            selected_tags = ("__all__", )

        if request.accepted_renderer.format == "html":
            tags = Tag.objects.all()
            data = response.data
            recipes = data.get("results")
            context = {
                "recipes": recipes,
                "tags": tags,
                "selected_tags": selected_tags,
                "title": title,
            }
            return Response(context, template_name="recipes.html")
        return response


class WebsiteRecipeFavouriteViewSet(RecipeFavouriteViewSet):
    authentication_classes = (SessionAuthentication, )


class WebsiteShoppingCartViewSet(ShoppingCartViewSet):
    authentication_classes = (SessionAuthentication, )
