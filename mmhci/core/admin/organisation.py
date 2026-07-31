from django.contrib import admin

from mmhci.core.models.organisation import organisation_address
from mmhci.core.models.organisation import organisation_form_template
from mmhci.core.models.organisation import organisation_policy
from mmhci.core.models.organisation import organisation_role_policy
from mmhci.core.models.organisation import organisation_user_role
from mmhci.core.models.organisation import organisation

admin.site.register(organisation_address)
admin.site.register(organisation_form_template)
admin.site.register(organisation_policy)
admin.site.register(organisation_role_policy)
admin.site.register(organisation_user_role)
admin.site.register(organisation)
