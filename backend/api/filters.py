from django_filters import rest_framework as filters

from .models import Recipe


class RecipeFilter(filters.FilterSet):
    is_favorited = filters.BooleanFilter(field_name="favourites",
                                         method="get_is_favorited")
    is_in_shopping_cart = filters.BooleanFilter(
        field_name="to_shopping",
        method="get_is_in_shopping_cart",
    )
    tags = filters.CharFilter(field_name="tags__slug",
                              lookup_expr="exact")

    class Meta:
        model = Recipe
        fields = ('tags', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value:
            return (Recipe.objects.filter(favourites__user=user)
                    .order_by("-pub_date"))
        return Recipe.objects.all().order_by("-pub_date")

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value:
            return (Recipe.objects.filter(to_shopping__user=user)
                    .order_by("-pub_date"))
        return Recipe.objects.all().order_by("-pub_date")