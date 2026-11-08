from django.test import TestCase
from django.urls import reverse


class HealthCheckTests(TestCase):
    def test_health_check(self):
        response = self.client.get(reverse("health"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        self.assertEqual(response.json()["service"], "raglab-api")