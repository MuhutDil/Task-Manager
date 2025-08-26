import json
import os

from django.test import TestCase
from django.urls import reverse

from .models import CustomUser

entities_file = os.path.join('task_manager', 'fixtures', 'entities_data.json')


class CustomUserTest(TestCase):
    fixtures = ["users.json"]

    @classmethod
    def setUpTestData(cls):
        cls.initial_count = CustomUser.objects.count()
        cls.user = CustomUser.objects.get(pk=1)
        cls.list_url = reverse("users_list")

    def setUp(self):
        self.client.force_login(self.user)
        with open(entities_file) as file:
            self.setup_data = json.loads(file.read())['users']

    def test_user_list(self):
        response = self.client.get(self.list_url)
        users = response.context["users"]
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.list_url)
        self.assertTrue(len(users) == self.initial_count)

    def test_user_create(self):
        create_url = reverse("users_create")
        login_url = reverse("login")
        flash_message = "User registered successfully."
        new_user = self.setup_data['new']

        # post user data with redirect on login page
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(create_url, new_user, follow=True)
        self.assertRedirects(response, login_url)
        self.assertContains(response, flash_message, status_code=200)
        
        # check added user
        response = self.client.get(self.list_url)
        users = response.context["users"]
        self.assertTrue(len(users) == self.initial_count + 1)
        self.assertContains(response, new_user["username"])

    def test_user_update(self):
        update_url = reverse("users_update", kwargs={"pk": self.user.id})
        old_name = self.user.username
        update_user = self.setup_data["update"]
        new_username = update_user["username"]
        flash_message = "User successfully updated."

        # post updated data
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(update_url, update_user, follow=True)
        self.assertRedirects(response, self.list_url)
        self.assertContains(response, flash_message, status_code=200)
        
        # check updated data
        response = self.client.get(self.list_url)
        self.assertContains(response, new_username)
        self.assertNotContains(response, old_name)

    def test_user_delete(self):
        delete_url = reverse("users_delete", kwargs={"pk": self.user.id})
        username = self.user.username
        flash_message = "User successfully deleted."

        # get delete page
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)

        # post delete page
        response = self.client.post(delete_url, follow=True)
        self.assertRedirects(response, self.list_url)
        self.assertContains(response, flash_message, status_code=200)   

        # check deleted user
        response = self.client.get(self.list_url)
        users = response.context["users"]
        self.assertTrue(len(users) == self.initial_count - 1)
        self.assertNotContains(response, username)
