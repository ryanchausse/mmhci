"""
NB: similar to Referrer and some elements are in ReferredTo, but also Organisation
Formerly named in the UI as "Provider"
"""

from django.apps import AppConfig


class PractitionerConfig(AppConfig):
    name = "mmhci.apps.practitioner"
