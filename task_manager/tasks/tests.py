from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import CustomUser

from .models import Task, TaskLabel


class TaskTest(TestCase):
    fixtures = [
        "tasks.json",
        "users.json",
        "statuses.json",
        "labels.json",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.initial_count = Task.objects.count()
        cls.user = CustomUser.objects.get(pk=1)
        cls.task = Task.objects.get(pk=1)
        cls.status = Status.objects.get(pk=1)
        cls.label = Label.objects.get(pk=1)
        cls.list_url = reverse("tasks_list")
        cls.task_data = {
            "name": "test task 3",
            "description": "some description",
            "status": 1,
            "author": 1,
            "labels": (1, 2),
        }

    def setUp(self):
        self.client.force_login(self.user)

    def test_task_list(self):
        response = self.client.get(self.list_url)
        tasks = response.context["tasks"]
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.list_url)
        self.assertTrue(len(tasks) == self.initial_count)
        
    def test_task_filter(self):
        filter_data = {"status": 1, "labels": 1}
        response = self.client.get(self.list_url, filter_data)
        tasks = response.context["tasks"]
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(self.list_url)
        self.assertTrue(len(tasks) == 1)
        self.assertFalse(len(tasks) == 2)
    
    def test_task_filter_empty(self):
        filter_data = {"status": 2, "executor": 1}
        response = self.client.get(self.list_url, filter_data)
        tasks = response.context["tasks"]
        self.assertTrue(len(tasks) == 0)
        self.assertFalse(len(tasks) == 2)

    def test_task_create(self):
        create_url = reverse("tasks_create")
        flash_message = "Task successfully created."

        # create task
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(create_url, self.task_data, follow=True)
        self.assertRedirects(response, self.list_url)
        self.assertContains(response, flash_message, status_code=200)

        # check added task
        response = self.client.get(self.list_url)
        tasks = response.context["tasks"]
        self.assertContains(response, "test task 3")
        self.assertTrue(len(tasks) == self.initial_count + 1)

    def test_task_detail(self):
        detail_url = reverse("tasks_detail", kwargs={"pk": self.task.id})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(detail_url)
        self.assertContains(response, self.task)
        self.assertContains(response, self.status)
        self.assertContains(response, self.user)
        self.assertContains(response, self.label)
        task_label_count = TaskLabel.objects.filter(task=self.task).count()
        self.assertEqual(task_label_count, 2)

    def test_task_update(self):
        old_name = self.task.name
        new_name = "new test task"
        update_url = reverse("tasks_update", kwargs={"pk": self.task.id})
        flash_message = "Task successfully updated."

        # update task
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 200)
        self.task_data["name"] = new_name
        self.task_data["labels"] = [1]
        response = self.client.post(update_url, self.task_data, follow=True)
        self.assertRedirects(response, self.list_url)
        self.assertContains(response, flash_message, status_code=200)
        
        # check updated task
        detail_url = reverse("tasks_detail", kwargs={"pk": self.task.id})
        response = self.client.get(detail_url)
        task_label_count = TaskLabel.objects.filter(task=self.task).count()
        self.assertContains(response, new_name)
        self.assertContains(response, self.status)
        self.assertContains(response, self.user)
        self.assertContains(response, self.label)
        self.assertEqual(task_label_count, 1)
        self.assertNotContains(response, old_name)

    def test_task_delete(self):
        task_name = self.task.name
        delete_url = reverse("tasks_delete", kwargs={"pk": self.task.id})
        flash_message = "Task successfully deleted."

        # delete task
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(delete_url, follow=True)
        self.assertRedirects(response, self.list_url)
        self.assertContains(response, flash_message, status_code=200)
        
        # check deleted tasks
        response = self.client.get(self.list_url)
        tasks = response.context["tasks"]
        self.assertTrue(len(tasks) == self.initial_count - 1)
        self.assertNotContains(response, task_name)
