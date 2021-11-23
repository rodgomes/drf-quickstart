from django.urls import include, path

from rest_framework import routers

from api import views

app_name = "api"

router = routers.SimpleRouter()
router.register("persons", views.PersonViewSet, basename="persons")
router.register("reminders", views.ReminderViewSet, basename="reminders")


urlpatterns = [
    path("", include(router.urls)),
]
