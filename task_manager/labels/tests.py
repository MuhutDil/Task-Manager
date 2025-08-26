import json
import os

from django.test import TestCase
from django.urls import reverse

from task_manager.users.models import CustomUser

from .models import Label

entities_file = os.path.join('task_manager', 'fixtures', 'entities_data.json')


class LabelTest(TestCase):
    fixtures = [
        "labels.json",
        "users.json",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.initial_count = Label.objects.count()
        cls.user = CustomUser.objects.get(pk=1)
        cls.label = Label.objects.get(pk=1)
        cls.list_url = reverse("labels_list")

    def setUp(self):
        self.client.force_login(self.user)
        with open(entities_file) as file:
            self.setup_data = json.loads(file.read())['labels']

    def test_label_list(self):
        response = self.client.get(self.list_url)
        labels = response.context["labels"]
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.list_url)
        self.assertTrue(len(labels) == self.initial_count)

    def test_label_create(self):
        create_url = reverse("labels_create")
        new_label = self.setup_data["new"]
        flash_message = "Label successfully created."

        # create label
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(create_url, new_label, follow=True)
        self.assertRedirects(response, self.list_url)
        self.assertContains(response, flash_message, status_code=200)

        # check added label
        response = self.client.get(self.list_url)
        labels = response.context["labels"]
        self.assertContains(response, new_label["name"])
        self.assertTrue(len(labels) == self.initial_count + 1)

    def test_label_update(self):
        old_name = self.label.name
        update_label = self.setup_data["update"]
        new_name = update_label["name"]
        update_url = reverse("labels_update", kwargs={"pk": self.label.id})
        flash_message = "Label successfully updated."

        # update label
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(update_url, update_label, follow=True)
        self.assertRedirects(response, self.list_url)
        self.assertContains(response, flash_message, status_code=200)

        # check updated label
        response = self.client.get(self.list_url)
        self.assertContains(response, new_name)
        self.assertNotContains(response, old_name)

    def test_label_delete(self):
        label_name = self.label.name
        delete_url = reverse("labels_delete", kwargs={"pk": self.label.id})
        flash_message = "Label successfully deleted."

        # delete label
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(delete_url, follow=True)
        self.assertRedirects(response, self.list_url)
        self.assertContains(response, flash_message, status_code=200)

        # check deleted label
        response = self.client.get(self.list_url)
        labels = response.context["labels"]
        self.assertTrue(len(labels) == self.initial_count - 1)
        self.assertNotContains(response, label_name)