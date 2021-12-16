from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.core import mail
from django.conf import settings

from Simplemooc.courses.models import Course

# Create your tests here.

class ContactCourseTest(TestCase):

    def setUp(self):
        self.course = Course.objects.create(name='Django',slug='django')

    def tearDown(self):
        self.course.delete

    # Os dois métodos acima são chamados no início e no fim do teste
    
    def test_contact_email(self):
        data = {'name' : 'fulando de tal', 'email' : '', 'message' : ''}
        client = Client()
        path = reverse('course:details', args=[self.course.slug])
        response = client.post(path, data)
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório')
        self.assertFormError(response, 'form', 'message', 'Este campo é obrigatório')

    def test_contact_form_sucess(self):
        data = {'name' : 'fulano de tal', 'email' : 'admin@gmail.com', 'message': 'Olá'}
        client = Client()
        path = reverse('courses:details', args=[self.course.slug])
        response = client.post(path,data)
        self.assertEqual(len(mail.outbox))
        self.assertEqual(mail.outbox[0].to, [settings.CONTACT_EMAIL])

