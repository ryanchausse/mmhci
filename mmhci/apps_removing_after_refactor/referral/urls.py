from django.urls import path

from . import views

app_name = "referral"
urlpatterns = [
    path("", views.index, name="index"),
]
