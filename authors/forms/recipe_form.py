from pyexpat import model
from django import forms
from recipes.models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ['is_published', 'author',
                   'preparation_steps_is_html', 'slug']
