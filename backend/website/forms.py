from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from api.models import Recipe, RecipeIngredientsDetails

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email")


IngredientsFormSet = forms.inlineformset_factory(
    Recipe,
    RecipeIngredientsDetails,
    fields="__all__",
    can_delete=False,
    min_num=2,
    max_num=50,
    extra=0,
)


class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    """Форма с чекбоксами."""
    template_name = "widgets/checkbox_select.html"


class RecipeCreateForm(forms.ModelForm):
    """Создание/редактирование рецепта."""
    class Meta:
        model = Recipe
        exclude = ("author", "ingredients")
        widgets = {
            "tags": CustomCheckboxSelectMultiple(),
        }
