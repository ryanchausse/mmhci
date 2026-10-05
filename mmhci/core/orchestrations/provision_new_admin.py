# This is meant to run after the new org is created, which requires only the new
# org record to be created in the admin section.
# Requires OrchestrationPermissions -> "core.provision_new_admin_user"
# This orchestration will, on submission of a form from a View:
# 1. Add a new user as the Admin
# 2. Add new records:
#      - OrgGroup Admins
#      - OrgRole Admin
#      - OrgGroupMembership <new user> to Admins
#      - 
# Permissions are:
# - Audit Log
#       - view log entry
#     - Address
#       - all
#     - Announcement
#       - all
#     - AssessmentMeasurement
#      - all
#     - AssessmentReferral
#      - all
#     - AssessmentType
#      - all
#     - MeasurementTypeAssessmentType
#      - all
#     - Consent
#      - all
#     - Contact
#      - all
#     - ContactAttempt
#      - all
#     - ContactConsent
#      - all
#     - ContactNote
#      - all
#     - ContactPerson
#      - all
#     - ContactRequest
#      - all
#     - ContactUpload
#      - all
#     - FormTemplate
#      - all
#     - Measurement
#      - all
#     - MeasurementType
#      - all
#     - Note
#      - all
#     - Organisation
#      - view
#      - change
#      - add
#     - OrganisationAddress
#      - all
#     - OrganisationFormTemplate
#      - all
#     - OrganisationGroup
#      - all
#     - OrganisationGroupMembership
#      - all
#     - OrganisationRole
#      - all
#     - Person
#      - all
#     - PersonAddress
#      - all
#     - PersonAvailability
#      - all
#     - Practitioner
#      - all
#     - PractionerAddress
#      - all
#     - PractitionerOrganisation
#      - all
#     - Referral
#      - all
#     - ReferralConsent
#      - all
#     - ReferralEvent
#      - all
#     - ReferralUpload
#      - all
#     - SMS
#      - all
#     - SmsEvent
#       - add, view, change
#     - SmsFormTemplate
#      - all
#     - Survey
#      - all
#     - Tag
#      - all
#     - Upload
#      - all
#     - Users
#      - all, incl. active flag

# # Provisioning method:
# from django.contrib.auth.models import Group, Permission
# from django.contrib.contenttypes.models import ContentType
# from myapp.models import Invoice, Client, Receipt

# # 1. Get or create your role
# manager_role, _ = Group.objects.get_or_create(name="Billing Manager")

# # 2. Get the content types for the entire app or specific models
# models = [Invoice, Client, Receipt]
# content_types = ContentType.objects.get_for_models(*models).values()

# # 3. Pull ALL default permissions for these models implicitly
# permissions = Permission.objects.filter(content_type__in=content_types)

# # 4. Bind them to the role in one database hit
# manager_role.permissions.set(permissions)




from django.db import transaction
from mmhci.core.models.organisation import Organisation
from mmhci.core.models.person import Person
from mmhci.core.services.core.auditlog_base import AuditLogBaseService
from mmhci.core.services.core.org_permissions_required_base import OrgPermissionsRequiredBaseService

class CreatePersonService(AuditLogBaseService, OrgPermissionsRequiredBaseService):
    # Business rule validation lives in single-domain (model) services.
    # Multiple model/multi-stage orchestrations can import multiple
    # single-domain services.
    required_permissions = frozenset({'core.add_person'})

    def __init__(self, request, data):
        AuditLogBaseService.__init__(self, request)
        OrgPermissionsRequiredBaseService.__init__(self, request.org_perms)
        self.request = request
        self.data = data

    @transaction.atomic
    def execute(self):
        # Does this user have permission to add a Person in their
        # current org? Current org id should be set in middleware
        current_org = Organisation.objects.get(
            pk=self.request.session.get("current_org_id")
        )
        if not self.request.session.get("current_org_id") in self.authorized_org_ids:
            raise PermissionError("You cannot create a Person in the current org.")

        with self.audit_write():
            person = Person.objects.create(
                first_name=self.data["first_name"],
                last_name=self.data["last_name"],
                preferred_name=self.data["preferred_name"],
                dob=self.data["dob"],
                phone=self.data["phone"],
                email=self.data["email"],
                owning_organisation=current_org
            )

        return person
