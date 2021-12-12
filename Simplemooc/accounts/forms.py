from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms.widgets import PasswordInput
#Essas duas linhas são necessárias já que há um modelo personalizado padrão para usuário
User = get_user_model()

class RegisterForm(forms.ModelForm):

    email = forms.EmailField(label = 'E-Mail')
    password1 = forms.CharField(label='Senha', widget=PasswordInput)
    password2 = forms.CharField(label='Confirmação de senha', widget=PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'], code='password_mismatch'
                )
        return password2

    def save(self, commit=True): # Método para salvar o email do usuário separadamente(não padrão)
        user = super(RegisterForm, self).save(commit = False)

        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'email']

class EditAccountForm(forms.ModelForm):

    # O método clean_email não é necessário, já que o form é custom

    class Meta:
        model = User
        fields = ['username', 'name', 'email']


#O seguinte trecho é utilizado se o usuário for o padrão do Django

'''class RegisterForm(UserCreationForm):

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

class EditAccountForm(forms.ModelForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        query_set = User.objects.filter(email=email).exclude(pk = self.instance.pk)
        #Verifica se o email ja foi utilizado, com exceção ao do usuário
        
        if query_set.exists(): #O .exists é necessário
            raise forms.ValidationError('Este email ja está sendo utilizado')
        
        return email

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']'''



