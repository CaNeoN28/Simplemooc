from django import forms
from django.core.mail import send_mail
from django.conf import settings

class ContactCourse(forms.Form):
    name = forms.CharField(label='Nome', max_length=100)
    email = forms.EmailField(label='Email')

    message = forms.CharField(label='Mensagem/Dúvida', widget=forms.Textarea)
    #O widget define a forma da entrada, já que não há um form.TextField

    #É possível usar o argumento required = False para atributos opcionais 

    def send_mail(self, course):
        subject = '[%s] Curso', course
        message = 'Nome: %(name)s;Email: %(email)s;Mensagem: %(message)s'
        context = {
            'name' : self.cleaned_data['name'],
            'email': self.cleaned_data['email'],
            'message': self.cleaned_data['message']
        } #Atribui os dados do email

        message = message % context #Formata os dados do email

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.CONTACT_EMAIL])