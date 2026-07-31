from django.contrib import admin

from mmhci.core.models.assessment import *

admin.site.register(AssessmentMeasurement)
admin.site.register(AssessmentReferral)
admin.site.register(AssessmentTypeMeasurementType)
admin.site.register(AssessmentType)
admin.site.register(Assessment)
admin.site.register(MeasurementType)
admin.site.register(Measurement)
