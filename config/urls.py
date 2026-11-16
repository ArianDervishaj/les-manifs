from django.conf import settings
from django.contrib import admin
from django.urls import path

from events import views

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("robots.txt", views.robots_txt),
]
