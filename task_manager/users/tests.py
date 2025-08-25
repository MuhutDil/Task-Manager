from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from .models import CustomUser


class CustomUserTest(TestCase):
    fixtures = ["users.json"]

    @classmethod
    def setUpTestData(cls):
        cls.initial_count = CustomUser.objects.count()
        cls.user = CustomUser.objects.get(pk=1)
        cls.list_url = reverse("users_list")
        cls.user_data = {
            "first_name": "name30",
            "last_name": "name31",
            "username": "testuser102",
            "password1": "password100",
            "password2": "password100",
        }

    def setUp(self):
        self.client.force_login(self.user)

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

        # post user data with redirect on login page
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(create_url, self.user_data, follow=True)
        self.assertRedirects(response, login_url)
        self.assertContains(response, flash_message, status_code=200)
        
        # check added user
        response = self.client.get(self.list_url)
        users = response.context["users"]
        self.assertTrue(len(users) == self.initial_count + 1)
        self.assertContains(response, self.user_data["username"])

    def test_user_update(self):
        update_url = reverse("users_update", kwargs={"pk": self.user.id})
        old_name = self.user.username
        new_name = "new_name"
        flash_message = "User successfully updated."

        # post updated data
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 200)
        updated_data = self.user_data.copy()
        updated_data["username"] = new_name
        response = self.client.post(update_url, updated_data, follow=True)
        self.assertRedirects(response, self.list_url)
        self.assertContains(response, flash_message, status_code=200)
        
        # check updated data
        response = self.client.get(self.list_url)
        self.assertContains(response, new_name)
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
