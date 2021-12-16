from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

# Create your tests here.

class HomeViewTest(TestCase):

    # As funções teste devem ter o nome de teste_alguma_coisa
    
    def test_home_status_code(self):
        client = Client() # Inicializa o cliente
        response = client.get(reverse('core:home')) # Recebe a url da view do core:home
        self.assertEqual(response.status_code, 200) # Método de teste

    def test_home_template_used(self):
        client = Client()
        response = client.get(reverse('core:home'))
        self.assertTemplateUsed(response, 'home.html')
        self.assertTemplateUsed(response, 'base.html')

        # Verifica se os templates home e base são usados na view core:home