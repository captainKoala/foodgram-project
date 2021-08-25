from django import template

from api.models import RecipeFavourite, RecipeShoppingCart

register = template.Library()


@register.filter
def add_class(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def filter_class(field, cls_prefix):
    """Удаляет из словаря с атрибутами для тега все классы, кроме начинающихся
    с префикса cls_prefix.
    """
    attrs = field.get("attrs")
    if attrs:
        _class = attrs.get("class")
        if _class:
            classes = " ".join(c.replace(cls_prefix, "")
                               for c in _class.split()
                               if c.startswith(cls_prefix))
            field["attrs"]["class"] = classes
    return field


@register.filter()
def is_recipe_in_shopping_cart(recipe, user):
    return RecipeShoppingCart.objects.filter(recipe=recipe, user=user).exists()


@register.filter()
def is_recipe_in_favorites(recipe, user):
    return RecipeFavourite.objects.filter(recipe=recipe, user=user).exists()
