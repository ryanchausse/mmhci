from django.contrib import admin

from mmhci.core.models.assessment import assessment_measurement
from mmhci.core.models.assessment import assessment_referral
from mmhci.core.models.assessment import assessment_type_measurement_type
from mmhci.core.models.assessment import assessment_type
from mmhci.core.models.assessment import assessment
from mmhci.core.models.assessment import measurement_type
from mmhci.core.models.assessment import measurement

admin.site.register(assessment_measurement)
admin.site.register(assessment_referral)
admin.site.register(assessment_type_measurement_type)
admin.site.register(assessment_type)
admin.site.register(assessment)
admin.site.register(measurement_type)
admin.site.register(measurement)
