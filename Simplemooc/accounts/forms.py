from django.contrib.auth import forms
from django.contrib.auth.forms import UserCreationForm
from django import forms

class RegisterForm(UserCreationForm):

    email = forms.EmailField(label = 'E-Mail') #Adiciona email como field do form

    def save(self, commit=True): # Método para salvar o email do usuário separadamente(não padrão)
        user = super(RegisterForm, self).save(commit = False) # Não salva o usuário padrão
        user.email = self.cleaned_data['email'] # Atribui o email ao usuário

        if commit:
            user.save()
        
        return user