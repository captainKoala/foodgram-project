import requests

from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, HttpResponse
from django.urls import reverse


def index(request):
    """ Главная страница сайта. """
    base_url = "http://" + str(get_current_site(request))
    recipes_url = base_url + reverse("recipes-list") + "?tags=dinner&tags=lunch"
    tags_url = base_url + reverse("tags-list")

    recipes = requests.get(recipes_url).json()["results"]
    print(recipes)
    tags = requests.get(tags_url).json()

    context = {
        "tags": tags,
        "recipes": recipes,
    }

    return render(request, "index.html", context=context)
