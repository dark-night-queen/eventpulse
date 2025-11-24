# Standard Library imports
from django.urls import path

# App imports
from apps.common.views import health, test_event

urlpatterns = [
    path("health/", health, name="health"),
    path("test/event/", test_event, name="test_event"),
]
