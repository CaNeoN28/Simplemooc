from django import forms

class ContactCourse(forms.Form):
    name = forms.CharField(label='Nome', max_length=100)
    email = forms.EmailField(label='Email')

    message = forms.CharField(label='Mensagem/Dúvida', widget=forms.Textarea)
    #O widget define a forma da entrada, já que não há um form.TextField

    #É possível usar o argumento required = False para atributos opcionais 