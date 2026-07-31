from django.urls import path

from mmhci.core.views.form_template import form_template

urlpatterns = [
    path("", form_template.index, name="index"),
]
