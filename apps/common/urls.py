# Standard Library imports
from django.urls import path

# App imports
from apps.common.views import health

urlpatterns = [
    path("health/", health, name="health"),
]
