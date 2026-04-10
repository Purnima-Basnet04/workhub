import unittest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from users.models import Profile
from jobs.models import Job
from companies.models import Company
from skills.models import Skill

class WorkHubFeatureTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile = Profile.objects.create(user=self.user)
        self.skill = Skill.objects.create(name='Python')
        self.company = Company.objects.create(name='TestCompany')
        self.job = Job.objects.create(title='Test Job', company=self.company, min_experience=0)

    def test_user_registration_and_login(self):
        response = self.client.post('/user/register/', {
            'username': 'newuser', 'password1': 'pass1234', 'password2': 'pass1234', 'email': 'new@user.com'
        })
        self.assertIn(response.status_code, [200, 302])
        login = self.client.login(username='testuser', password='testpass')
        self.assertTrue(login)

    def test_profile_creation_and_update(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get('/user/profile/')
        self.assertEqual(response.status_code, 200)

    def test_job_listing_and_detail(self):
        response = self.client.get('/jobs/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(f'/jobs/{self.job.id}/')
        self.assertEqual(response.status_code, 200)

    def test_job_application_flow(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(f'/jobs/{self.job.id}/applications', {})
        self.assertIn(response.status_code, [200, 302])

    def test_skill_assignment(self):
        self.profile.skills.add(self.skill)
        self.assertIn(self.skill, self.profile.skills.all())

    def test_company_profile(self):
        response = self.client.get(f'/companies/{self.company.id}/')
        self.assertIn(response.status_code, [200, 302])

    def test_resume_generation(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(f'/user/resume/{self.profile.id}')
        self.assertEqual(response.status_code, 200)

    def test_notifications(self):
        # Placeholder: Implement notification creation and retrieval test
        pass

    def test_admin_panel_access(self):
        admin = User.objects.create_superuser('admin', 'admin@test.com', 'adminpass')
        self.client.login(username='admin', password='adminpass')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
