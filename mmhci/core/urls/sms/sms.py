from django.urls import path

from mmhci.core.views.sms import sms

urlpatterns = [
    path("", sms.index, name="index"),
]
