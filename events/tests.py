from django.conf import settings
from django.test import RequestFactory, TestCase
from django.urls import reverse

from .security import client_ip


class SecurityHeadersTests(TestCase):
    def test_headers(self):
        response = self.client.get("/robots.txt", secure=True)
        self.assertIn("default-src 'none'", response["Content-Security-Policy"])
        self.assertIn("frame-ancestors 'none'", response["Content-Security-Policy"])
        self.assertEqual(response["X-Frame-Options"], "DENY")
        self.assertEqual(response["X-Content-Type-Options"], "nosniff")
        self.assertEqual(response["Referrer-Policy"], "same-origin")


class AdminTests(TestCase):
    def test_admin_lives_under_the_secret_url(self):
        self.assertTrue(reverse("admin:index").startswith(f"/{settings.ADMIN_URL}"))

    def test_login_lockout_after_5_failures(self):
        url = reverse("admin:login")
        attempt = {"username": "nobody", "password": "wrong"}
        for _ in range(5):
            self.client.post(url, attempt, HTTP_X_REAL_IP="203.0.113.7", secure=True)
        self.assertEqual(
            self.client.post(url, attempt, HTTP_X_REAL_IP="203.0.113.7", secure=True).status_code,
            429,
        )
        # Another visitor is not affected.
        self.assertEqual(
            self.client.post(url, attempt, HTTP_X_REAL_IP="203.0.113.8", secure=True).status_code,
            200,
        )


class ClientIpTests(TestCase):
    def test_prefers_the_header_set_by_caddy(self):
        rf = RequestFactory()
        self.assertEqual(client_ip(rf.get("/", HTTP_X_REAL_IP="203.0.113.7")), "203.0.113.7")
        self.assertEqual(client_ip(rf.get("/")), "127.0.0.1")


class RobotsTests(TestCase):
    def test_robots_txt(self):
        response = self.client.get("/robots.txt", secure=True)
        self.assertEqual(response["Content-Type"], "text/plain")
        self.assertNotContains(response, settings.ADMIN_URL)
