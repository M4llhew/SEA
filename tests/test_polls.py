from django.db import models
from django.test import TestCase
from django.urls import reverse

from polls.models import CustomerUser
from polls.models import Task


class ViewsTestCase(TestCase):
    def setUp(self):
        self.user = CustomerUser.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

    def test_login_view(self):
        response = self.client.get(reverse('polls:Login'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('polls:Login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)

    def test_create_comment_form(self):
        task = Task.objects.create(Title='Test Task', Desc='Test Description', Alias_Assigned=self.user)
        response = self.client.post(reverse('polls:create_comment', args=(task.Task_ID,)),
                                    {'Comment': 'Test Comment'})
        self.assertEqual(response.status_code, 302)

    def test_display_choices(self):
        alias_assigned_field = Task._meta.get_field('Alias_Assigned')
        if isinstance(alias_assigned_field, models.ForeignKey):
            choices_queryset = alias_assigned_field.related_model.objects.all()
            for obj in choices_queryset:
                print(obj.username)
        elif alias_assigned_field.choices:
            for choice in alias_assigned_field.choices:
                print(choice[0])
        else:
            print("Field doesn't have choices.")

    def test_task_create(self):
        response = self.client.post(reverse('polls:task_create'),
                                    {'Title': 'Test Task', 'Desc': 'Test Description',
                                     'Alias_Assigned': 'testuser',
                                     'Progress': 'TODO'})
        self.assertEqual(response.status_code, 400)

    def test_user_create(self):
        response = self.client.post(reverse('polls:user_create'),
                                    {'first_name': 'John', 'last_name': 'Doe', 'username': 'newuser',
                                     'password': 'newP4ssword!'})
        self.assertEqual(response.status_code,
                         200)

    def test_logout_view(self):
        response = self.client.get(reverse('polls:logout'))
        self.assertEqual(response.status_code, 302)

    def test_display_users(self):
        response = self.client.get(reverse('polls:display'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task Management')

    def test_login_view_invalid_credentials(self):
        response = self.client.post(reverse('polls:Login'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertNotEqual(response.status_code, 302)
