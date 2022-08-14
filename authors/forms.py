from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


# adicionar atributos no campo
def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)

# validção do django.


def strong_password(value):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    if not regex.match(value):
        raise ValidationError(
            'Password must have at least one uppercase letter,'
            'one lowercase letter and one number.'
            'The length should be at least 8 characters', code='invalid',)


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr(self.fields['username'], 'placeholder', 'Your username')
        add_attr(self.fields['username'], 'class', 'username')
        add_placeholder(self.fields['first_name'], 'Ex.: john')
        add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        add_placeholder(self.fields['email'], 'Ex.: email@example.com')

    # sobre escrevendo formulrios
    first_name = forms.CharField(
        error_messages={'required': 'Write your first name'},
        required=True,
        label='First name',
        max_length=150
    )
    last_name = forms.CharField(
        error_messages={'required': 'Write your last name'},
        required=True,
        label='Last name',
        max_length=150
    )

    email = forms.EmailField(
        required=True,
        error_messages={'required': 'This field is required.'},
        label='E-mail',
        help_text='The e-mail must be valid'

    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Type your password',
            'type': 'password',
        }),
        error_messages={
            'required': 'Password must not be empty',
        },
        help_text=(
            'Password must have at least one uppercase letter,'
            'one lowercase letter and one number.'
            'The length should be at least 8 characters'
        ),
        label='Password',
        validators=[strong_password]
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password',
            'type': 'password',
        }),
        error_messages={
            'required': 'Confirm Password must not be empty',
        },
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        ]
       # exclude = ['first_name', 'last_name']
        labels = {
            'username': 'Username',
            'email': 'E-mail',

        }
        # modificando help_texts
        """  help_texts = {
            'email': 'The e-mail must be valid'
        } """

        error_messages = {
            'username': {
                'required': 'This field is required',
                'max_length': 'This',
                'invalid': 'This field is not a valid email address'
            }
        }

        # modificar campos de um formulario
        widgets = {
            'first_name': forms.TextInput(attrs={
                # 'placeholder': 'Seu primeiro nome',
                'class': 'input text-input',
            }),
            'password': forms.PasswordInput(attrs={
                'type': 'password',
            })
        }

    # validando campos clean_name = expecifico para aquele campo
    def clean_password(self):
        data = self.cleaned_data.get('password')
        text = 'password'
        if text in data:
            raise ValidationError(
                'Não digite %(value)s no campo password',
                code='invalid',
                params={'value': f'{text}'}
            )

        return data

    # validação em geral metodo super().
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'Password and password2 must be equal',
                code='invalid'
            )
            raise ValidationError({
                # 'password': 'Password and password2 must be equal',
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                ],

            }, code='invalid',)
