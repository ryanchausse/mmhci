from django.urls import path

from mmhci.core.views.upload import upload

urlpatterns = [
    path("", upload.index, name="index"),
]
