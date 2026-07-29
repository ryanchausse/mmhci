from django.urls import path

from . import views

app_name = "third_party_service"
urlpatterns = [
    path("", views.index, name="index"),
]
