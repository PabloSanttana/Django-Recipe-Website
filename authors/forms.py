from django import forms
from django.contrib.auth.models import User


# adicionar atributos no campo
def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_attr(self.fields['username'], 'placeholder', 'Your username')
        add_attr(self.fields['username'], 'class', 'username')
        add_placeholder(self.fields['first_name'], 'Your first name')

    # sobre escrevendo password
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password',
            'type': 'password',
        }),
        error_messages={
            'required': 'Password must not be empty',
        },
        help_text=(
            'Password must have at least one uppercase letter,'
            'one lowercase letter and one number.'
            'The length should be at least 8 characters'
        )
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password',
            'type': 'password',
        })
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
            'email': 'Email',
            'password': 'Password',
            'first_name': 'First name',
            'last_name': 'Last name'
        }
        help_texts = {
            'email': 'The e-mail must be valid'
        }

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
