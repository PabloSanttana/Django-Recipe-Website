from django import forms
from recipes.models import Recipe
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


class RecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr(self.fields['preparation_steps'],
                 'placeholder', 'How to prepare a  recipe')
        add_attr(self.fields['preparation_steps'],
                 'class', 'span-2')

    title = forms.CharField(
        max_length=150,
        min_length=4,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Recipe Title',
        }),
        error_messages={
            'required': 'This field is required',
            'min_length': 'Make sure the value is at least 4 characters',
            'max_length': 'Make sure the value is a maximum of 10 characters.'
        }
    )

    description = forms.CharField(
        max_length=150,
        min_length=4,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Description recipe',
        }),
        error_messages={
            'required': 'This field is required',
            'min_length': 'Make sure the value is at least 4 characters',
            'max_length': 'Make sure the value is a maximum of 10 characters.'
        }
    )

    class Meta:
        model = Recipe
        exclude = ['is_published', 'author',
                   'preparation_steps_is_html', 'slug']

        error_messages = {

            'preparation_time': {
                'required': 'This field is required'
            },
            'preparation_time_unit': {
                'required': 'This field is required'
            },
            'servings': {
                'required': 'This field is required'
            },
            'servings_unit': {
                'required': 'This field is required'
            },
            'preparation_steps': {
                'required': 'This field is required'
            },
            'category': {
                'required': 'This field is required'
            },
        }
        widgets = {
            "cover": forms.FileInput(
                attrs={
                    'class': 'span-2',
                    'accept': "image/*",
                    'onchange': 'validateSize(this)'
                },
            ),
            'servings_unit': forms.Select(
                choices=(
                    ("Pessoas", 'Pessoas'),
                    ("Porções", 'Porções'),
                    ("Pedaços", 'Pedaços'),
                ),
                attrs={
                    'placeholder': 'Select servings unit'
                }
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ("Minutos", 'Minutos'),
                    ("Horas", 'Horas'),
                ),
                attrs={
                    'placeholder': 'Recipe preparation time unit'
                }
            )
        }

        help_texts = {
            'cover': 'Maximum size file ( 2MB )'
        }

    def clean_category(self):
        data = self.cleaned_data.get('category')
        if data is None:
            raise ValidationError('This field is required', code='invalid')

        return data

    def clean_preparation_time(self):
        data = self.cleaned_data.get('preparation_time')
        if data <= 0:
            raise ValidationError('Invalid number', code='invalid')

        return data

    def clean_servings(self):
        data = self.cleaned_data.get('servings')
        if data <= 0:
            raise ValidationError('Invalid number', code='invalid')

        return data

    def clean_cover(self):
        data = self.cleaned_data.get('cover')
        if data is None:
            raise ValidationError(
                'This field is requiredor or Maximum size reached ( 2MB )',
                code='invalid',
            )
        else:
            megabyte = 1024 * 1024
            if data.size / megabyte > 2:
                raise ValidationError(
                    'Maximum size reached ( 2MB )',
                    code='invalid',
                )
        return data
