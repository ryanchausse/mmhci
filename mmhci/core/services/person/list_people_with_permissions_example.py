from mmhci.core.models.person import Person
from mmhci.core.services.core.org_permissions_required_base import OrgPermissionsRequiredBaseService


# Note that the user's org_perms dict is in the view or celery layer
class ListPeopleService(OrgPermissionsRequiredBaseService):
    required_permissions = frozenset(
        # Can add more necessary permissions
        {"core.view_person"}
    )

    def execute(self):
        # I think that this select_related() is potentially leaky. Possibly better
        # to have an orchestrated service run a second query to a "get org" service
        # that accepts a list of orgs and returns data based on the scoped permission
        # the user has from the OrgPermissionRequiredBaseService
        return Person.objects.filter(
            organisation_id__in=self.authorized_org_ids
        ).select_related("organisation")
