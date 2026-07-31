from django.urls import path

from mmhci.core.views.referral import referral

urlpatterns = [
    path("", referral.index, name="index"),
]
