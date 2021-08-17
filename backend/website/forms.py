from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

from api.models import Recipe, RecipeIngredientsDetails
# from users.models import User

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email")


IngredientsFormSet = forms.inlineformset_factory(
    Recipe,
    RecipeIngredientsDetails,
    fields="__all__",
    can_delete=True,
    min_num=2,
    max_num=50,
    # widgets={
    #     "ingredient": autoc,
    # },
)


class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    template_name = "widgets/checkbox_select.html"


class RecipeCreateForm(forms.ModelForm):
    # ingredients = forms.ModelChoiceField(
    #     queryset=Ingredient.objects.all(),
    #     widget=autocomplete.ModelSelect2Multiple(url="ingredient-autocomplete"),
    # )

    class Meta:
        model = Recipe
        # exclude = ("author", )
        exclude = ("author", "ingredients")
        widgets = {
            "tags": CustomCheckboxSelectMultiple(),
            # "ingredients": autocomplete.ModelSelect2(url="ingredient-autocomplete")
            # "ingredients": IngredientWidget(),
        }
