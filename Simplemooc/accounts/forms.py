from django.contrib.auth import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegisterForm(UserCreationForm):

    email = forms.EmailField(label = 'E-Mail') #Adiciona email como field do form

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists(): # Verifica se o email ja está cadastrado
            raise forms.ValidationError('Email já cadastrado!') # Retorna um erro se o email ja estiver cadastrado
        
        return email

    def save(self, commit=True): # Método para salvar o email do usuário separadamente(não padrão)
        user = super(RegisterForm, self).save(commit = False) # Não salva o usuário padrão
        user.email = self.cleaned_data['email'] # Atribui o email ao usuário

        if commit:
            user.save()
        
        return user