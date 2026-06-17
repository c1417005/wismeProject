from django.test import TestCase
from django.urls import reverse

from wisme.tests.test_legacy import make_verified_user


class HealthCheckAPITest(TestCase):
    """/api/v1/health/ の疎通と認証制御を確認する。"""

    def setUp(self):
        self.url = reverse('api:health')

    def test_returns_200_for_authenticated_user(self):
        user = make_verified_user('health@example.com', 'Testpass123!')
        self.client.force_login(user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'ok')

    def test_returns_403_for_unauthenticated_user(self):
        # DRF の IsAuthenticated は未認証時に 403 を返す
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
