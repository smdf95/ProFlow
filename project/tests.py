from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Project

# Create your tests here.

class ProjectTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        cls.project = Project.objects.create(
            created_by=cls.user,
            name='Test Project',
            description='This is a test project',
            start_date='2022-01-01',
            due_date='2022-12-31',
            status='active',
            priority='high',
            assigned_users=[cls.user]
        )

        def test_project_content(self):
            project = Project.objects.get(id=1)
            expected_author = f'{project.created_by}'
            expected_name = f'{project.name}'
            expected_description = f'{project.description}'
            expected_start_date = f'{project.start_date}'
            expected_due_date = f'{project.due_date}'
            expected_status = f'{project.status}'
            expected_priority = f'{project.priority}'
            expected_assigned_users = f'{project.assigned_users.all()}'
            self.assertEqual(expected_author, 'testuser')
            self.assertEqual(expected_name, 'Test project')
            self.assertEqual(expected_description, 'This is a test project')
            self.assertEqual(expected_start_date, '2022-01-01')
            self.assertEqual(expected_due_date, '2022-12-31')
            self.assertEqual(expected_status, 'active')
            self.assertEqual(expected_priority, 'high')
            self.assertEqual(expected_assigned_users, 'testuser')

        def test_project_str_method(self):
            project = Project.objects.get(id=1)
            self.assertEqual(str(project), project.name)

        def test_get_absolute_url(self):
            project = Project.objects.get(id=1)
            self.assertEqual(project.get_absolute_url(), reverse('project-detail', args=[project.id]))


class projectViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.project = Project.objects.create(
            created_by=self.user,
            name='Test Project',
            description='This is a test project',
            start_date='2022-01-01',
            due_date='2022-12-31',
            status='active',
            priority='high',
            assigned_users=[self.user]
        )

    def test_project_list_view(self):
        url = reverse('project-home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is a test project')
        self.assertTemplateUsed(response, 'project/home.html')

    def test_project_detail_view(self):
        url = reverse('project-detail', args=[self.project.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.name)

    def test_create_project_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('project-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project_form.html')

        response = self.client.project(reverse('project-create'), {
            'name': 'New title',
            'description': 'New text',
            'start_date': '2022-01-01',
            'due_date': '2022-12-31',
            'status': 'active',
            'priority': 'high',
            'assigned_users': [self.user]
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Project.objects.filter(name='New title').exists())

    def test_update_project_view(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('project-update', kwargs={'pk': self.project.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project_form.html')

        response = self.client.project(url, {
            'name': 'Updated title',
            'description': 'Updated text',
            'start_date': '2022-01-02',
            'due_date': '2022-12-30',
            'status': 'inactive',
            'priority': 'low',
            'assigned_users': 'admin'
        })
        self.project.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.project.name, 'Updated title')

    def test_delete_project_view(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('project-delete', kwargs={'pk': self.project.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project/project_confirm_delete.html')

        response = self.client.project(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())
