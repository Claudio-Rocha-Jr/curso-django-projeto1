import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()

def add_placeholder(field,placeholder_val):
    add_attr(field, 'placeholder',placeholder_val)

def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    
    if not regex.match(password):
        raise ValidationError ((
            'Password failed regex'),
            code='invalid'
        )

class RegisterForm(forms.ModelForm):

    # password2 = forms.CharField(
    # required=True,
    # widget=forms.PasswordInput(attrs = {
    #     'placeholder':'Repeat your password'
    # })
    # ) -----> Sobrescre o campo

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_placeholder(self.fields['username'],'Your username')
        add_placeholder(self.fields['email'],'Your e-mail')
        add_placeholder(self.fields['first_name'],'Ex.: John')
        add_placeholder(self.fields['last_name'],'Ex.: Doe')
        # add_attr(self.fields['username'],'css','a-css-class')
        #add_attr(self.fields['email'],'placeholder','Your E-mail')
        #self.fields['username'].widget.attrs['placeholder'] = 'Que legal'

    #SE ALTERAR INDIVIDUAMENTE ELE SOBRESCREVE (PRIORIDADE) OU UTILIZAR INIT PARA ACRESCENTAR OU META PARA FAZER EM LOTE
    username = forms.CharField(
        label = 'Username',
        error_messages = {
            'required': 'This field must not be empty',
            'max_length': 'This field must have less or equal than 150 characters',
            'min_length': 'Username must have at least 4 characters',
            'invalid': 'This field is invalid'
        },
        help_text =	'Username must have letters, number or one of these @.+-',
        min_length=4, max_length=150
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs = {
            'placeholder':'Repeat your password'
        }),
        error_messages={
            'required': 'Passwords must match'
        },
        help_text = (
            'Password must be strong'
        ),
        label = 'Password2'
        )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs = {
            'placeholder':'Your password'
        }),
        error_messages={
            'required': 'Type your password'
        },
        help_text = (
            'Password must be strong'
        ),
        label = 'Password',
        validators=[strong_password]
        )

    first_name = forms.CharField(
        error_messages= {
            'required':'Write your first name'
        },
        required = True,
        label= 'First Name'
    )
    last_name = forms.CharField(
        error_messages= {
            'required':'Write your last name'
        },
        required = True,
        label= 'Last Name'
    )
    email = forms.EmailField(
        error_messages = {
            'required': 'E-mail must not be empty',
        },
        label= 'E-mail',
        help_text = 'The e-mail must be valid'
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
        #exclude = ['first_name'] - Return all fiends except
        # labels = {
        #     # 'username': 'Username', #Change field label
        #     # 'first_name':'First Name', 
        #     # 'last_name': 'Last Name',
        #     'email':'E-mail',
        # }
        # help_texts = {
        #     'email': 'The e-mail must be valid'
        # }
        error_messages = {
            'username':{
                'required': 'This field must not be empty',
                'max_length': 'This field must have less than 3 characters',
                'invalid': 'This field is invalid'
            },
            # 'email':{
            #     'required':'E-mail must not be empty'
            # }
        }
        # widgets = {
        #     'password': forms.PasswordInput(attrs = {
        #         'placeholder': 'Type your password here'
        #     })
        # }

    # def clean_password(self):
    #     data = self.cleaned_data.get('password')

    #     if 'atenção' in data:
    #         raise ValidationError(
    #             'Não digite %(value)s no campo password',
    #             code = 'invalid',
    #             params = {'value': '"atenção"'}
    #         )

    #     return data

    # def clean_first_name(self): #Método especial para validação do campo
    #     data = self.cleaned_data.get('first_name')

    #     if 'John Doe' in data:
    #         raise ValidationError(
    #             'Não digite %(value)s no campo first name',
    #             code = 'invalid',
    #             params = {'value': '"John Doe"'}
    #         )

    #     return data

    def clean_email(self):
        email = self.cleaned_data.get('email','')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError('User e-mail is already in use', code='invalid')

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'Password and password2 must match!',
                code = 'invalid'
                )

            raise ValidationError({
                'password': password_confirmation_error,
                'password2':[password_confirmation_error]
                #'Another error'
            })
