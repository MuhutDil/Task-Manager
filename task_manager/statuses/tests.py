from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from task_manager.users.models import CustomUser

from .models import Status


class StatusTest(TestCase):
    fixtures = [
        "statuses.json",
        "users.json",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.initial_count = Status.objects.count()
        cls.user = CustomUser.objects.get(pk=1)
        cls.status = Status.objects.get(pk=1)
        cls.list_url = reverse("statuses_list")

    def setUp(self):
        self.client.force_login(self.user)

    def test_status_list(self):
        response = self.client.get(self.list_url)
        statuses = response.context["statuses"]
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.list_url)
        self.assertTrue(len(statuses) == self.initial_count)

    def test_status_create(self):
        create_url = reverse("statuses_create")
        flash_message = 'Status successfully created.'
        status_data = {"name": "test status 3"}

        # create status
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(create_url, status_data, follow=True)
        self.assertRedirects(response, self.list_url)
        self.assertContains(response, flash_message, status_code=200)
        
        # check added status
        response = self.client.get(self.list_url)
        statuses = response.context["statuses"]
        self.assertContains(response, "test status 3")
        self.assertTrue(len(statuses) == self.initial_count + 1)

    def test_status_update(self):
        old_name = self.status.name
        new_name = "new test status"
        status_data = {"name": new_name}
        flash_message = 'Status successfully updated.'
        update_url = reverse("statuses_update", kwargs={"pk": self.status.id})

        # update status
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(update_url, status_data, follow=True)
        self.assertRedirects(response, self.list_url)
        self.assertContains(response, flash_message, status_code=200)

        # check updated status
        response = self.client.get(self.list_url)
        self.assertContains(response, new_name)
        self.assertNotContains(response, old_name)

    def test_status_delete(self):
        status_name = self.status.name
        flash_message = "Status successfully deleted."
        delete_url = reverse("statuses_delete", kwargs={"pk": self.status.id})

        # delete status
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(delete_url, follow=True)
        self.assertRedirects(response, self.list_url)
        self.assertContains(response, flash_message, status_code=200)

        # check deleted status
        response = self.client.get(self.list_url)
        statuses = response.context["statuses"]
        self.assertTrue(len(statuses) == self.initial_count - 1)
        self.assertNotContains(response, status_name)