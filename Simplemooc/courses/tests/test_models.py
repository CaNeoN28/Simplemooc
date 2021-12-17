from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.core import mail
from django.conf import settings

from Simplemooc.courses.models import Course

from model_bakery import baker

class CourseManagerTestCase(TestCase):

    def setUp(self):
        self.courses_django = baker.make('courses.Course', _quantity=5, name='Python para web com django')
        self.courses_dev = baker.make('courses.Course', _quantity=10, name='Python para Devs')
        self.client = Client()
    
    def tearDown(self):
        Course.objects.all().delete()

    def test_courses_search(self):
        search = Course.objects.search('django')
        self.assertEqual(len(search), 5)
        search = Course.objects.search('dev')
        self.assertEqual(len(search), 10)
        search = Course.objects.search('python')
        self.assertEqual(len(search), 15)