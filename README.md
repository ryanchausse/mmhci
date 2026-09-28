# MMHCI

This is an attempt to refactor our existing apps into the Django framework.

Each model will get a created_at, updated_at, created_by, and updated_by.

Ruff settings will remain cranked to maintain strict standards.

## TL;DR

The most important takeaways:

- Models don't import anything
- Services only import models from their own domain / bounded context
- Orchestrations only import from services to execute cross-functional workflows

Stand up local development server:
`docker compose -f docker-compose.local.yml up`

Pull the docker compose down before bringing it back up (Ctrl+C to stop local containers
can fail to exit cleanly):
`docker compose -f docker-compose.local.yml down`

Rebuild with new pip packages:
`uv lock` / `uv sync` for local
`docker compose -f docker-compose.local.yml up --build --force-recreate --renew-anon-volumes django`

## Motivation

We frequently confuse our data model / schema with our UI, and speak directly to our
users about the underlying database, tables, and fields. These discussions should
instead be a conversation about interfaces and business rules, with the core data model
sorted out internally by the software development team.

We have FUD around deployments because of ripple effects/unforeseen side effects to
changes made in our app at present. A re-architecture will head off most of the time we
spend "thinking about what could go wrong".

It would be obvious about where to look to understand, change or add code based on a
disciplined approach to design patterns. This will help improve our feature velocity
and prevent things like bespoke queries that implement point-in-time business logic
rules that may change with time and are difficult to find in aggregate.

We have an increasing number of lines of code and a large app becomes increasingly
difficult to reason about. Refactoring using better encapsulation and naming can improve
things such as cognitive load and the bus factor.

We don't have an automatic updated_at, created_at, and their equivalent *_by on each
DB table. This will help us to understand the order of events.

We have too many indices in our tables whereas we should rely on the query planner to
optimise our queries.

Deployment is complicated because our CI/CD pipelines don't do much testing and we don't
have a reliable mechanism to prevent breaking changes from being merged into main. We
should also squash on merge to prevent a polluted commit history - main currently has
commits with messages like "fix typos", making it unclear when a particular feature or
fix was put in place, which is only partially solved by searching through our GitHub
issue history.

Other apps/repositories access the database directly. We should instead implement an
interface such as an API with things like rate limiting so we can measure and ensure
performance. A read-only replica would probably help, as well as CQRS.

I have many more notes but I feel these are some main wins.

## Getting started
- Follow the guide at https://cookiecutter-django.readthedocs.io/en/latest/2-local-development/developing-locally-docker.html#before-getting-started
- Become familiar with uv as python version/package/environment manager. Do not use poetry or pip.
- Might need to run `uv python install 3.14`


## Command to run in Docker locally
At root: `docker compose -f docker-compose.local.yml up`

Accessible (according to current config) at http://127.0.0.1:8005/


## Example to run other commands in docker container, e.g. 'manage.py makemigrations'
Might have to run these after initial docker-compose up:

`docker compose -f docker-compose.local.yml run --rm django uv lock`
NB: rebuild after adding a package; might have to restart.

`docker compose -f docker-compose.local.yml run --rm django python manage.py migrate`

`docker compose -f docker-compose.local.yml run --rm django python manage.py createsuperuser`


## Architecture Explained

Each app is a domain/bounded context. There is a services directory in each to do
work that applies to its own area (e.g. Referral has a "create_referral" service that
pulls in the model, does whatever business logic checks that are needed related directly
to the Referral domain).

We should be cautious of circular imports. The way to avoid this is to have more or less
unidirectional flows:

- A model does not import any other model or service
- A domain service can import models located in the same app
- An orchestration service can import multiple domain services but not models directly

That way the graph is one way: no imports contain imports that import from the first
import (yo dawg, I heard you like imports...)


### Example of service architecture

So, let's say you wanted to record a person's consent to create a referral.

The model for ReferralConsent, the relational table, relates equally to the Consent and
Referral domains, so the model is located in the main, core app:
- core/models.py

There is core app service to create a ReferralConsent DB record. This service imports
the Referral service, which uses the Referral model. Same for Consent.

To illustrate the application of business rules:

We should not be able to create a Consent for a Referral if the Referral's status is
"abandoned", so when the orchestration service:
- core/services/orchestration/create_referral_consent_with_notification.py

...imports a Referral service from the Referral app:
- apps/referral/services/is_not_closed.py

...the "is_not_closed" service performs the Referral-specific business logic check
for the given Referral instance. It imports the Referral model:
- apps/referral/models.py

...and implements all the logic needed to validate that the Referral is in an acceptable
state.

In this case, one of the validation rules might be that the Referral's status is not
"completed", so the operation can proceed. It might also check that the "is_deleted"
field is not True as well. More rules can easily be added over time without needing to
change or worry about logic that may be present in other areas of the app. This is an
example of encapsulated, domain-local business rule validation.

When it comes to creating a ReferralConsent record, because this will involve
logic in apps which cross domain boundaries (e.g. Consent is another app), we need to
place the "create referral consent" service into a higher, common, orchestration layer.

This orchestration service will live in the top level core app:
- core/services/orchestration/

Orchestration services will contain only the logic related to cross-domain actions and
in reality they will probably contain most of our business logic in general.

For example, perhaps we need to check that the Consent and Referral records are in
compatible states in only certain combinations. We would import services from each
app/domain to perform that check in this top level cross-domain service.

Thus, imports in the cross-domain orchestration service:
- core/services/orchestration/create_referral_consent_with_notification.py

...will import services from the Referral, SMS, Person, Log, and Consent app, apply
cross-domain business logic rules such as "a Person must have an SMS number to
be able to Consent to a referral being created", and will attempt to create all
relevant records in an atomic fashion, i.e., the service will roll back the
entire transaction across all domains if any one service throws an error.

This means, for example, that a ReferralConsent record can't be created without the
successful creation of a Log record.


## Orchestration and preventing circular import errors

For anything crossing domain boundaries, a service should be created in the
orchestration service layer. This will head off most circular import problems.

Django also has some checks included in the framework that attempt to check for these
types of problems, which is an example of why we should be using Django instead of
Flask, but I digress.

If we are disciplined about putting things that most closely relate to a Referral in the
Referral app, and to Contact in the Contact app, we can cleanly separate concerns.

Once or if the core/services/orchestration/ directory becomes too large and difficult to
understand, we can break things out into sub-orchestration directories that are grouped
or named by either:

1) what we consider to be similar business logic, or by
2) cross-domain names

E.g.:

1) core/services/orchestration/intake_from_external_web_form/, or
   core/services/orchestration/refer_to_provider/

or:

2) core/services/orchestration/contact_referral/, or
   core/services/orchestration/referral_provider/

These might be bad examples. Maybe I can update them when this becomes relevant.

For now, we can create services like:

1) core/services/orchestration/create_contact_with_person_and_referral.py
2) core/services/orchestration/update_organisation_policy_and_send_to_sekhmet.py

Orchestration services should ideally be used where the "owning" app is unclear, as in,
responsibility is equally shared across apps/domains where third party APIs are called,
and where there are complicated, multistep workflows. Here, to prevent circular imports
and to maintain clarity, anything cross-domain should probably be placed in an
orchestration. This is a more sustainable pattern as the app grows.


### Naming

It's important that we use consistent naming principles. Some nomenclature rules:

1) Use CRUD names for CRUD operations. Use "create", "update", and "delete" as verbs for
   functions.
2) GET operations are a little different. For functions that we expect to return either
   one record or "not found" or a "more than one record found" Exception, such as the
   Django-native DoesNotExist exception, use "get". For functions that we expect to
   return 0 to many items, use "find".


### Templates and Template Partials

Using the Jinja2 templating engine, we will create a base layout and fill in only what
we need to change for each page. The goal is to create a consistent visual language that
doesn't surprise users on each new page.


### UI/UX

Basically, the goal is to make this web app as similar to Excel as possible, so users
are already familiar with the paradigm, get trained easily, don't worry too much about
making mistakes, and can intuit where to go to perform an action. The app should be
essentially an Excel experience + rigorous checks for data integrity, permissions,
workflows, etc.

For now and the foreseeable future, we'll continue to use Bootstrap and avoid SPA
frontend frameworks, because they are likely not needed.

To the maximum extent possible, we should make our front end templates "dumb" and our
frontend logic nonexistent.


### Specific architecture notes

- Use Celery to perform long-running actions, and HTMX to poll for completion of those
  actions in order to update UI elements. Polling is not ideal, but this is the simplest
  and easiest paradigm. Celery is also great in that it can assign relative priority
  to tasks, meaning we can do things like send data to a rate-limited external service
  or do more computationally heavy work with lower priority so that we can do more
  important or time sensitive tasks more quickly. This also uses multiprocessing rather
  than multithreading which is better in a non-I/O context.
- CI/CD needs implementation that tears down and builds our project so we can ensure
  immutable deployments
- DB transactions will be atomic (e.g. if a Log isn't created, we don't also create
  a DB record)
- We can use select_related() to prevent N+1 queries. That is currently a big
  performance killer. In some cases, it may be better to have a few round trips with
  simple SELECT queries, or just "give me everything and I will filter with Python"
- RBAC will involve more layers of indirection so we can intercept at each layer to
  enforce business logic related to Organisation, Role, Provider, User, Policy, etc.
- We will not actually delete a record, but mark as deleted. Will create actual deletion
  policy later on in consultation with CAB and other relevant advisors and for legal
  compliance.
- A connection pool for DB connections is essential. During deployment to AWS, we might
  choose to use the RDS Proxy service.
- The API layer(s) will use Django-Ninja
- In model definitions, place PK field(s) at the top of the attribute list, then FKs,
  then model-specific attributes. Every model gets metadata fields by inheritance from
  the custom base class (created_by, updated_at, etc.)


## Development notes on permissions/RBAC

We can partially leverage Django's native cacheing for user permissions and use the
Django-native PermissionRequired mixin. Django fetches all user permissions for the
has_perm() function on the first time it is queried, on a per HTTP request round trip
basis. This latter piece might not work for us, however.

Will use a middleware class to ensure all routes are @login_required by default, then a
PermissionRequiredMixin to all views. Like so (Gemini):

#### views.py
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView
from .models import Article

class ArticleListView(PermissionRequiredMixin, ListView):
    model = Article
    template_name = 'articles/list.html'

    # Define the required permission using 'app_label.codename'
    permission_required = 'articles.view_article'

    # Customise behavior when access is denied
    login_url = '/login/'
    redirect_field_name = 'next'


#### PermissionRequiredMixin override class

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from myapp.models import UserRole, TenantPermission, ObjectOverride

class FineGrainedRBACMixin(PermissionRequiredMixin):
    """
    Custom mixin that overrides Django's default permission system
    to query multiple tables for fine-grained access control.
    """
    # You can still use this as a variable target for your queries
    permission_required = 'edit_article'

    def has_permission(self):
        user = self.request.user

        # 1. Always allow superusers (optional but standard)
        if user.is_superuser:
            return True

        # 2. Extract context from the request (e.g., URL parameters)
        tenant_id = self.kwargs.get('tenant_id')
        object_id = self.kwargs.get('pk')

        # 3. Table 1 Check: Global User Roles
        # Example: Check if user has an 'Admin' or 'Editor' role record
        has_role = UserRole.objects.filter(
            user=user,
            role_name__in=['Admin', 'Editor']
        ).exists()

        if not has_role:
            return False

        # 4. Table 2 Check: Tenant/Organization Boundaries
        # Example: Ensure the user belongs to the specific company/tenant route
        has_tenant_access = TenantPermission.objects.filter(
            user=user,
            tenant_id=tenant_id,
            action=self.permission_required
        ).exists()

        if not has_tenant_access:
            return False

        # 5. Table 3 Check: Specific Object Blacklists/Overrides
        # Example: Check if this specific user has been explicitly blocked from this row
        is_blocked = ObjectOverride.objects.filter(
            user=user,
            object_id=object_id,
            access_level='DENIED'
        ).exists()

        if is_blocked:
            return False

        # If all multi-table database checks pass, grant access
        return True

#### and in the view:

from django.views.generic import UpdateView
from myapp.models import Article

class ArticleUpdateView(FineGrainedRBACMixin, UpdateView):
    model = Article
    template_name = 'articles/edit.html'
    fields = ['title', 'content']

    # Used by your mixin's custom query logic
    permission_required = 'edit_article'
    raise_exception = True


### Logging
Offload logging to Celery as we block views via this RBAC policy, so logging, as long as
dead letter queues and retry logic are configured correctly, should not be dropped. It's
very costly to INSERT on every page READ so that might be an adequate way to do this for
now. I don't want to use a no-SQL database, so we'll she how far we can push Postgres in
the meantime.

### Front-end
https://adminlte.io/themes/v4/index.html
Free under MIT licence and available for commercial theft (use)


### Existing major use cases / functionality

Functions present in our PMHCIS app that don't map to PMHC-MDS (prob. non-exhaustive)
- A unified search bar for Contacts/Clients|Referrals by name, initials, phone, DOB
- Create New Contact/Client|Referral
- View incomplete Contact/Client|Referral
- Assign owning org to Referral
- Assign permissions/RBAC/org to user/org/role/policy
  - this can override default permissions "policy" for each role pertaining to a
    resource in an org
- View Reports -> Contacts
  - input pathways, PII, outcome, created_by, assigned to org, minutes spent
- View Reports -> Referrals
  - last updated/dates, status, pathway, suburb, IAR-DST results, suicide flag, notes,
    assigned to org/user, input pathway, outcome, PHN if org not PHN, time spent, hours
    spent
- View Reports -> Abandoned Referrals
  - date, status, pathway, IAR-DST level, abandon reason, notes, org, created_by, hours
    spent
- View Reports -> "Callback Requests"
  - contact outcomes and pathways
  - contact outcome by PHN and pathway
  - outcomes of "converted callbacks"
    - (when Contacts get a Referral [and are "converted" to a Client], they will/may
      have a Referral outcome)
- "Inbox" with "Incoming Referrals"
  - this seems to be a sort of staging area. We expose an interface for clients to use
    an API (Delta API?) to send us data for merging into our system; this seems also to
    accept the input of the external-facing web form that we host in a different
    location. The user can review and import each record ("convert to a Referral" -> not
    the same as converting a Contact/Client to a Referral within this internal web app
    though)
  - Each Referral ("eReferral" in our language for this staging area) has:
    - a status like converting/converted/new/declined
    - A source
    - date
    - name/DOB
    - suburb, suicide flag, IAR-DST level of care, referrer, assigned to
    - Things like Medicare card / NDIS data
    - IAR-DST data, risk assessment data
    - metadata like notes
    - Attachment files associated with the eReferral (maybe we can call these uploads)
    - "Activities", a really good log of what was done, by whom, and when (this is in
      our fat JavaScript on the Client side, which I would like to move into the server
      side)
- Dashboards -> Survey: charts based on patient-facing survey data (I felt listened to,
  overall experience likert measures, etc.)
  - Overall experience likert chart
  - experience over time likert chart
  - chart of positive feedback over time, filterable by date line chart
  - survey responses/% responded vs. time for PHN vs. national rate
- Dashboards -> Intake: charts based on activity by team member and filterable by date
  - Contacts created vs. time (aggregate among all team members or individual)
  - IAR-DSTs completed
  - Average assessment levels by domain (cool!)
  - Team member activity (does not seem implemented?), probably based on ActivityLog
- Ability to download PMHC-MDS data Intake in ZIP file format
- Ability to upload PMHC-MDS data in ZIP file format
- Ability to upload (I think these are rarely used):
  - Service model PDF file(?)
  - System & Telephony Support Process PDF(?)
  - Intake Survey Information PDF
  - Protecting PII in the PMHCIS Intake Module PDF
  - Offline Form Word file
  - Operations Manual PDF
- Ability to specify IAR-DST, Note, and SMS templates (with templates and a "mark as
  shared")
- A Client and Referral data quality check page (e.g. Records with missing data)
- A user account audit page, listing user activity:
  - User name
  - orgs
  - roles
  - records viewed per month
- A Tag entity system with CRUD
- Print a referral w/ obscured lines if user has no access to PII. Same for Contacts
- Links to various documentation/guides, most notably our help page/documentation which
  ships with the app
  - https://pmhcis-test.intake.org.au/help
- Basically all the rest, from what I can see, is admin stuff - create new org, assign
  to org, download list of orgs, upload list of orgs by CSV, edit user details like
  name, MFA toggle, change password, roles/org level permissions on CRUD operations,
  etc.

### More thinking about RBAC / permissions

Implicated models:
- User
- PermissionException
- Group
- Organisation
- Policy

Relational tables:
- UserPolicyException? UPDATE: no because this is implicit in the OrgPolicy
- UserOrganisationGroup (user's group context in the org)
- OrganisationPolicy
- GroupPolicy (default group policies)

... and also something like AccessException (UserRoleException?) which grants one-time
exceptions to the rules? I am not perfectly comfortable with this but I think that is
the full scope. We could also make exceptions time bound.

Permission flow:
- GET request
- LoginRequiredMiddleware ensures user is logged in
- Each View has FineGrainedPermissionMixin which accepts:
  - request.user to get the user profile. Might get permissions here too
  - the object being requested
- Then, the FineGrainedPermissionMixin:
  1. checks to see if user is a superuser (if so, provide access)
  2. checks to see if user has an exception to the required permissions UPDATE: no, User
     can be assigned to a group with n = 1
  3. checks to see if the org has a role permission exception
  4. checks base role permissions

The middleware returns a 403 wherever one of these layers denies the action. The Mixin
requires the organisation, the object, and the user to work (role, exception, and
policy can be derived from these)

Checking in FineGrainedPermissionMixin:

1. If User is superuser, return True
2. If specific User has an exception for permissions to this particular Object instance,
   and the exception time has not expired, return True UPDATE: no, because the User can
   be assigned to a Group with n=1. Checking datetimes for permissions can come later as
   this is a costly query and we can add that query later to Views themselves.
3. If the Org has a permission Policy on the Object being requested, for the
   OrganisationRole, get those and see if the User has/has not got access via the
   Organisation context. This is a return False or a return True.
4. Check base/default Role permissions systemwide

Further permissions can be sorted out in the view itself, combined with the Object model

Object here means model, Role would seem to map to Group

Model permissions can be added willy nilly and checked in the View

e.g. "can_export_contact_surnames" can be defined in the model's Meta permission set,
and the View would check whether the User has those permissions?

Should new "exception" groups be created instead of a particular user having a
particular permission exception? Seems like a group of 1 would be best there because
of ease of adding new exceptions. yeah that's better.

Yeah so here's the best way:

Custom Authorisation backend that takes into account three things:

- User
- Group
- Organisation

Can't I just make OrganisationGroups, as in the name of the Group? No. Too complex in
the long run.

Things like checking if the Referral originating / assigned Org can be done in the view
perhaps. Maybe not - Org policy should take into account if they want to customise this
behaviour. Should it be done by querying a Policy table, or could it be handled by a
model-based permission mapped to an Org? Prob the latter.

So yeah, in the end, just three things are needed, with Group permissions assignment
happening through the admin interface at first.

From Gemini:

#### backend.py:
from django.contrib.auth.backends import BaseBackend

class OrganizationPermissionBackend(BaseBackend):
    def has_perm(self, user_obj, perm, obj=None):
        # 1. Skip if user is inactive
        if not user_obj.is_active:
            return False

        # 2. Skip if no organization context is passed
        if obj is None or not hasattr(obj, 'organization'):
            return False

        # 3. Check membership and permissions within that organization
        org = obj.organization

        # Example logic: Adjust based on your Organization/Membership models
        return org.memberships.filter(
            user=user_obj,
            role__permissions__codename=perm
        ).exists()


#### settings/config
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default global perms
    'path.to.backends.OrganizationPermissionBackend',  # Your custom context perms
]

#### the view
def edit_document(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)

    # Django passes 'document' as the 'obj' argument to your backend
    if not request.user.has_perm('app.change_document', document):
        raise PermissionDenied

    # Proceed with view...

# !!This is how to do it. Finalised design!!

I don't think so. I submitted a further prompt that asked to associate Organisations with groups in a way that did not create a cross-product between Organisation and Group (i.e. group names like [org].[app].referral_edit)

It suggested an OrganisationGroup model something like:

#models.py:
from django.db import models
from django.contrib.auth.models import Group

class Organization(models.Model):
    name = models.CharField(max_length=255)

class OrganizationGroup(models.Model):
    # Links a standard, clean Django group to a specific organization
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='org_context')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='org_groups')

### Here, groups specific to the org would be uniquely named to the org like "nwmphn_clinician", not really getting around that, whereas default group names would be like "default_clinician" or something

##### custom Django-native backend to do auth
from django.contrib.auth.backends import BaseBackend

class ScopedGroupPermissionBackend(BaseBackend):
    def has_perm(self, user_obj, perm, obj=None):
        if not user_obj.is_active:
            return False
        if user_obj.is_superuser:
            return True

        # We explicitly require the organization context to be passed as 'obj'
        if obj is None or not isinstance(obj, Organization):
            return False

        # Query: Does the user belong to a group that:
        # 1. Belongs to THIS organization?
        # 2. Has THIS specific permission?
        return user_obj.groups.filter(
            org_context__organization=obj,
            permissions__codename=perm
        ).exists()

#### and in the view:
def edit_document(request, org_slug, doc_id):
    # 1. Fetch the organization context from the URL/Session
    organization = get_object_or_404(Organization, slug=org_slug)

    # 2. Fetch your clean, unlinked document
    document = get_object_or_404(Document, id=doc_id)

    # 3. Pass the organization instance as the 'obj' context
    if not request.user.has_perm('app.change_document', organization):
        raise PermissionDenied

    # Proceed to edit...


So basically, I'd pass the org relevant to the operation in this context. Might need to check up to two orgs in two steps, but it would seem not to be too often.

This is the way. Even works in the service layer context. Perfect!

##### Example service
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Document, Organization

class DocumentService:
    @staticmethod
    def update_document(user, org_slug, doc_id, new_data):
        """
        Handles the business logic and authorization for updating a document.
        """
        # 1. Fetch the organization context
        organization = get_object_or_404(Organization, slug=org_slug)

        # 2. Check permissions using your ScopedGroupPermissionBackend
        # This passes the Organization instance to the 'obj' argument
        if not user.has_perm('app.change_document', organization):I have the User, Group, and OrganisationGroup models for authorisation.

Use case 1: show user all data they should be able to see on dashboard

request comes in from user
get all groups and permissions for user
in view, call services that take the user with its cached permissions and shows data


Use case 2: allow user to update a model instance with a new value for a field

request comes in from user
get all groups and permissions for user
in view, must get the org to get the relevant permission, as no org FK exists on most tables
            raise PermissionDenied("You do not have permission to edit documents in this organization.")

        # 3. Fetch and update the document (which has no organization FK)
        document = get_object_or_404(Document, id=doc_id)

        for key, value in new_data.items():
            setattr(document, key, value)
        document.save()

        return document

#### and the corresponding view:
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .services import DocumentService

@require_POST
def edit_document_view(request, org_slug, doc_id):
    # Extract data from the request
    new_data = {"title": request.POST.get("title")}

    try:
        # Call the service layer
        updated_doc = DocumentService.update_document(
            user=request.user,
            org_slug=org_slug,
            doc_id=doc_id,
            new_data=new_data
        )
        return JsonResponse({"status": "success", "document_id": updated_doc.id})

    except PermissionDenied as e:
        return JsonResponse({"error": str(e)}, status=403)


...ScopedGroupPermissionBackend can live in app/backends.py. BaseBackend is django-native and has a contract with methods that can be overwritten. Prob important to keep the variable names in that example as-is.

Full suggested backends.py file (includes cacheing of user permissions per-request):

from django.contrib.auth.backends import BaseBackend
from .models import Organization  # Adjust the import to match your model path

class BaseObjectPermissionBackend(BaseBackend):
    """
    Handles global security checks and request-level query caching.
    """
    def has_perm(self, user_obj, perm, obj=None):
        if not user_obj.is_active:
            return False

        if user_obj.is_superuser:
            return True

        if obj is None:
            return False

        if not hasattr(user_obj, '_obj_perm_cache'):
            user_obj._obj_perm_cache = {}

        cache_key = (obj._meta.model_name, getattr(obj, 'pk', id(obj)), perm)

        if cache_key in user_obj._obj_perm_cache:
            return user_obj._obj_perm_cache[cache_key]

        result = self._has_obj_perm(user_obj, perm, obj)
        user_obj._obj_perm_cache[cache_key] = result
        return result

    def _has_obj_perm(self, user_obj, perm, obj):
        raise NotImplementedError("Subclasses must implement _has_obj_perm()")


class ScopedGroupPermissionBackend(BaseObjectPermissionBackend):
    """
    Validates permissions against organization-linked Django groups.
    """
    def _has_obj_perm(self, user_obj, perm, obj):
        # We explicitly require the organization context to be passed as 'obj'
        if not isinstance(obj, Organization):
            return False

        # Query: Does the user belong to a group that:
        # 1. Belongs to THIS organization?
        # 2. Has THIS specific permission?
        return user_obj.groups.filter(
            org_context__organization=obj,
            permissions__codename=perm
        ).exists()


### This one accepts multiple orgs and makes sure they all match (len())

from django.db.models import Count

class ScopedGroupPermissionBackend(BaseObjectPermissionBackend):
    """
    Validates permissions against organization-linked Django groups.
    """
    def _has_obj_perm(self, user_obj, perm, obj):
        # Handle a single Organization instance
        if isinstance(obj, Organization):
            target_orgs = [obj]

        # Handle an iterable of Organizations
        elif isinstance(obj, (list, tuple)) or hasattr(obj, '__iter__'):
            # Convert querysets or generators to a set of distinct instances or IDs
            # This ensures an accurate mathematical match and removes duplicates
            target_orgs = set(obj)
            
        else:
            return False

        # If an empty collection is passed, fail safely
        if not target_orgs:
            return False

        # Count how many unique target organizations the user has this permission for
        matching_orgs_count = Organization.objects.filter(
            id__in=[org.id for org in target_orgs],
            # Traverse reverse relation: Organization -> OrgContext -> Group -> User
            org_context__group__user=user_obj,
            org_context__group__permissions__codename=perm
        ).distinct().count()

        # The user has permission only if they match EVERY target organization
        return matching_orgs_count == len(target_orgs)


...must register in settings.py

I guess I could use the latter to display all org data on one page (maybe in separate
tables). The way to do that would be to supply all user orgs to the mixin, perhaps?

--------------------------------
So, I would put the following fields in the base model class(?):

org_originated
org_owned
org_assigned
is_active
is_deleted

but perhaps only certain models should have a base class with these

Then groups like "Org 1 Admins"

and then I'd do like the view:

from django.shortcuts import get_object_or_404

def delete_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Check the default delete permission against the row's assigned organization context
    if not has_org_permission(request.user, task.org_assigned_id, 'delete_task'):
        raise PermissionDenied("You cannot delete this item within this organization scope.")

    task.delete()
    ...

or

from django.core.exceptions import PermissionDenied
from django.shortcuts import render

def create_task_view(request, org_id):
    # Check if the user has the default 'add_task' permission in this specific org context
    if not has_org_permission(request.user, org_id, 'add_task'):
        raise PermissionDenied("You do not have permission to add tasks in this organization.")

    if request.method == "POST":
        # Safe to create the item because the context was validated up front
        Task.objects.create(
            title=request.POST['title'],
            org_origin_id=org_id,
            org_assigned_id=org_id
        )
        ...

and a util function for permissions checks:

def has_org_permission(user, org_id, perm_codename):
    """
    Checks if a user holds a default Django permission within a specific organization.
    
    Example: has_org_permission(request.user, 5, 'change_task')
    """
    if not user.is_active:
        return False
        
    if user.is_superuser:
        return True

    # Strip the app label if passed (e.g., 'myapp.change_task' -> 'change_task')
    if '.' in perm_codename:
        perm_codename = perm_codename.split('.')[-1]

    # Query: Is the user in a group that:
    # 1. Belongs to THIS specific organization?
    # 2. Holds THIS specific default Django permission?
    return user.groups.filter(
        organisationgroup__organization_id=org_id,
        permissions__codename=perm_codename
    ).exists()



another implementation:

# auth_backends.py
class OrganisationPermissionBackend:
    def authenticate(self, request, username=None, password=None):
        return None  # Only handles permissions, not login

    def has_perm(self, user_obj, perm, obj=None):
        # If no specific organisation object is passed, skip this backend
        if obj is None or not hasattr(obj, 'organisation'):
            return False
            
        # Check the user's role inside this specific organisation
        membership = user_obj.memberships.filter(organisation=obj).first()
        if not membership:
            return False

        # Map your custom permissions cleanly to roles
        if membership.role == 'ADMIN':
            return True  # Admins can do everything
            
        if membership.role == 'EDITOR' and perm in ['app.view_model', 'app.change_model']:
            return True
            
        if membership.role == 'VIEWER' and perm == 'app.view_model':
            return True

        return False

then settings.py:
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default global perms
    'path.to.OrganisationPermissionBackend',      # Your new row-level perms
]

then view:
# Django natively handles checking this specific row!
if request.user.has_perm('app.change_model', current_organisation):
    # Proceed with action

-------------

alternatively, to supply the org to a permission mixin:

from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin

class OrganisationPermissionMixin(LoginRequiredMixin):
    permission_required = None  # e.g., 'app.view_document'

    def get_organisation(self):
        """
        Override this method in individual views if the logic 
        to find the organisation changes.
        """
        # Default fallback: get it from the URL slug
        org_slug = self.kwargs.get('org_slug')
        return Organisation.objects.get(slug=org_slug)

    def dispatch(self, request, *args, **kwargs):
        # 1. Get the context-specific organisation
        org = self.get_organisation()

        # 2. Check the permission against that specific organisation
        if not request.user.has_perm(self.permission_required, org):
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


# Case 1: Simple list view using the URL slug
class DocumentListView(OrganisationPermissionMixin, ListView):
    permission_required = 'app.view_document'
    model = Document

# Case 2: Detail view where the org logic is different (fetched from the target object)
class DocumentDetailView(OrganisationPermissionMixin, DetailView):
    permission_required = 'app.change_document'
    model = Document

    def get_organisation(self):
        # Override the logic: Find the specific document first, then get its org
        document = self.get_object()
        return document.organisation

Note this presupposes an OrganisationPermissionBackend:
# auth_backends.py
class OrganisationPermissionBackend:
    def authenticate(self, request, username=None, password=None):
        return None  # Only handles permissions, not login

    def has_perm(self, user_obj, perm, obj=None):
        # If no specific organisation object is passed, skip this backend
        if obj is None or not hasattr(obj, 'organisation'):
            return False
            
        # Check the user's role inside this specific organisation
        membership = user_obj.memberships.filter(organisation=obj).first()
        if not membership:
            return False

        # Map your custom permissions cleanly to roles
        if membership.role == 'ADMIN':
            return True  # Admins can do everything
            
        if membership.role == 'EDITOR' and perm in ['app.view_model', 'app.change_model']:
            return True
            
        if membership.role == 'VIEWER' and perm == 'app.view_model':
            return True

        return False


--------------------
making this backend more dynamic:

from django.db import models
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

class Organisation(models.Model):
    name = models.CharField(max_length=255)

class Role(models.Model):
    name = models.CharField(max_length=100)  # e.g., "Editor", "Manager"
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='custom_roles')

    # Links directly to Django's native or custom model permissions
    permissions = models.ManyToManyField(Permission, blank=True)

    class Meta:
        # Prevents duplicate role names within the same organisation
        unique_together = ('name', 'organisation')

class OrganisationMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name='members')

    # Links the user to a dynamically managed database role
    role = models.ForeignKey(Role, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('user', 'organisation')


# auth_backends.py
class DynamicOrganisationPermissionBackend:
    def authenticate(self, request, username=None, password=None):
        return None

    def has_perm(self, user_obj, perm, obj=None):
        # Ensure we are checking permissions against an Organisation context
        if obj is None or not isinstance(obj, Organisation):
            return False
            
        # 1. Fetch the user's membership for this specific organisation
        membership = user_obj.memberships.filter(organisation=obj).select_related('role').first()
        if not membership:
            return False  # User is not a member of this organisation

        # 2. Extract the app_label and codename from the standard permission string (e.g., 'app.view_model')
        try:
            app_label, codename = perm.split('.')
        except ValueError:
            return False

        # 3. Check if the dynamic role has this permission assigned to it
        return membership.role.permissions.filter(
            codename=codename,
            content_type__app_label=app_label
        ).exists()


--------------------------------

Ok, so... building from first principles.

Models:
- User
- Organisation
- OrganisationGroup (Group specific to an org, strict org separation)
- OrganisationRole (Role specific to an org)
- OrganisationGroupRoleUser (links Users, OrganisationGroup, and OrganisationRole)
  - can also be called Membership or OrganisationMembership. Probably better.

from django.db import models
from django.contrib.auth.models import Permission  # Built-in Django permission system

class OrganisationRole(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="roles")
    name = models.CharField(max_length=100)  # e.g., "Admin", "Manager"
    
    # Add this: Links this company's custom role to granular permissions
    permissions = models.ManyToManyField(Permission, blank=True, related_name="organisation_roles")

    class Meta:
        unique_together = ('organisation', 'name')

    def __str__(self):
        return f"{self.organisation.name} - {self.name}"

# Inside your custom User model in models.py
class User(AbstractUser):
    # ... existing fields ...

    def has_org_permission(self, organisation_id, permission_codename):
        """
        Checks if the user belongs to any group inside the organization 
        that grants them the required permission via their assigned role.
        """
        # We query the Membership table to see if any valid row matches the criteria
        return self.memberships.filter(
            # 1. Scope it to the current organization
            organisation_group__organisation_id=organisation_id,
            # 2. Look through the role into its permissions many-to-many field
            organisation_role__permissions__codename=permission_codename
        ).exists()

# The mixin
from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied

class OrgPermissionRequiredMixin(AccessMixin):
    """
    Checks if the user has the required permission code via their 
    assigned role within the organization context.
    """
    required_permission = None  # Set this in your View (e.g., 'change_organisation')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        org_id = kwargs.get('organisation_id')
        if not org_id:
            raise PermissionDenied("Organisation context is missing from URL.")

        # Check permissions dynamically through the User helper method
        if not request.user.has_org_permission(org_id, self.required_permission):
            raise PermissionDenied("You do not have the required permissions in this organisation.")

        return super().dispatch(request, *args, **kwargs)

# Sample view
from django.views.generic import UpdateView
from .models import Organisation
from .permissions import OrgPermissionRequiredMixin

class OrganisationSettingsView(OrgPermissionRequiredMixin, UpdateView):
    model = Organisation
    template_name = "orgs/settings.html"
    fields = ['name']
    pk_url_kwarg = 'organisation_id'
    
    # Secure the view using the permission codename instead of a role name
    required_permission = "change_organisation" 


# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Organisation, OrganisationGroup, OrganisationRole, Membership

# 1. Manage Memberships inside the User page
class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 1  # Provides a blank row to easily add a new assignment

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [MembershipInline]

# 2. Make custom permissions easy to select with a dual-list box
@admin.register(OrganisationRole)
class OrganisationRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'organisation')
    list_filter = ('organisation',)
    filter_horizontal = ('permissions',)  # Adds the elegant left-to-right selection box

Would a view just check org permissions against available permissions for the user?
Maybe the Referral model should have permissions like "can_view_from_owning_org" and
"can_view_from_assigned_org". How, then, to work out when an org e.g. does not want to
ever let another org view its referrals? Maybe some bool flags on the models like
"can_access_from_another_org"? Or a separate permission with a similar name that
overrides access logic in the view?

e.g. role = get_object_or_404(OrganisationRole, id=role_id, organisation_id=organisation_id)


---

# Implementing a custom cache for user permissions per request (because this does not)
# Hold off on this for now.
# Inside your custom User model in models.py
class User(AbstractUser):
    # ... your existing code ...

    def has_org_permission(self, organisation_id, permission_codename):
        # 1. Initialize the cache dictionary on this user instance if it doesn't exist
        if not hasattr(self, '_org_perm_cache'):
            self._org_perm_cache = {}

        # Create a unique cache key combining the org and the permission
        cache_key = f"{organisation_id}:{permission_codename}"

        # 2. If we haven't checked this specific permission yet, query the database
        if cache_key not in self._org_perm_cache:
            has_perm = self.memberships.filter(
                organisation_group__organisation_id=organisation_id,
                organisation_role__permissions__codename=permission_codename
            ).exists()
            
            # Save the boolean result (True/False) to our cache
            self._org_perm_cache[cache_key] = has_perm

        # 3. Return the cached result
        return self._org_perm_cache[cache_key]


Would a view just check org permissions against available permissions for the user? Maybe the Referral model should have permissions like "can_view_from_owning_org" and "can_view_from_assigned_org"


-------------------------------

BaseBackend strategy for the above (hold off for now, shouldn't be too bad to get
perms on each request)

# myapp/backends.py
from django.contrib.auth.backends import BaseBackend
from .models import Organisation

class OrganisationPermissionBackend(BaseBackend):
    """
    Custom auth backend that routes standard Django permission checks
    through our multi-tenant OrganisationGroup, OrganisationRole, and Membership schema.
    """

    def has_perm(self, user_obj, perm, obj=None):
        # 1. Anonymous users have no multi-tenant permissions
        if not user_obj.is_authenticated:
            return False

        # 2. We expect the 'obj' argument to be the current Organisation instance
        if not isinstance(obj, Organisation):
            return False

        # 3. Extract the permission codename (Django permissions look like 'app_label.codename')
        if '.' in perm:
            _, permission_codename = perm.split('.', 1)
        else:
            permission_codename = perm

        # 4. Initialize request-level cache mirroring Django's native approach
        if not hasattr(user_obj, '_org_perm_cache'):
            user_obj._org_perm_cache = {}

        cache_key = f"{obj.id}:{permission_codename}"

        # 5. Query the database only if this specific check hasn't run during this request
        if cache_key not in user_obj._org_perm_cache:
            has_permission = user_obj.memberships.filter(
                organisation_group__organisation_id=obj.id,
                organisation_role__permissions__codename=permission_codename
            ).exists()
            
            user_obj._org_perm_cache[cache_key] = has_permission

        return user_obj._org_perm_cache[cache_key]

# myapp/mixins.py
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import get_object_or_404
from .models import Organisation

class OrgPermissionRequiredMixin(AccessMixin):
    org_permission = None

    def dispatch(self, request, *args, **kwargs):
        org = get_object_or_404(Organisation, id=kwargs.get('organisation_id'))
        
        if not request.user.has_perm(self.org_permission, obj=org):
            return self.handle_no_permission()
            
        request.organisation = org # Cache it on the request for easy access in your view
        return super().dispatch(request, *args, **kwargs)



# Updated model definitions for auth

from django.db import models
from django.contrib.auth.models import AbstractUser, Permission

# 1. User
class User(AbstractUser):
    pass

# 2. Organisation
class Organisation(models.Model):
    name = models.CharField(max_length=255)

# 3. OrganisationGroup
class OrganisationGroup(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="groups")
    name = models.CharField(max_length=100) # e.g., "Engineering", "Marketing"

    class Meta:
        unique_together = ('organisation', 'name')

# 4. OrganisationRole (Where permissions are assigned!)
class OrganisationRole(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="roles")
    name = models.CharField(max_length=100) # e.g., "Manager", "Viewer"
    
    # THIS IS THE EXACT ASSIGNMENT POINT
    # Connects this specific company role to Django's built-in system permissions
    permissions = models.ManyToManyField(Permission, blank=True, related_name="org_roles")

    class Meta:
        unique_together = ('organisation', 'name')

# 5. Membership
class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memberships")
    organisation_group = models.ForeignKey(OrganisationGroup, on_delete=models.CASCADE, related_name="members")
    organisation_role = models.ForeignKey(OrganisationRole, on_delete=models.CASCADE, related_name="members")

    class Meta:
        unique_together = ('user', 'organisation_group')

# How to assign permissions in code
# 1. Grab the permission you want to assign (e.g., native Django app permissions)
from django.contrib.auth.models import Permission
can_edit_billing = Permission.objects.get(codename="change_billing")

# 2. Fetch the specific role for that target organisation
from .models import OrganisationRole, Organisation
acme_corp = Organisation.objects.get(name="ACME Corp")
manager_role = OrganisationRole.objects.get(organisation=acme_corp, name="Manager")

# 3. ASSIGN IT HERE
manager_role.permissions.add(can_edit_billing)


--------------------------------

AUTHENTICATION_BACKENDS = [
    # 1. Keeps standard username/password logins and global permissions working
    'django.contrib.auth.backends.ModelBackend',

    # 2. Wire up your new organization-scoped group check
    'core.backends.ScopedGroupPermissionBackend',  # Change 'core' to your app name
]

To create OrganisationGroup records:
OrganizationGroup.objects.create(
    group=django_group,
    organization=instance
)

There was a suggestion to use a django Signal to detect creation of an organisation, which would then create groups based on org name and default group name, and add them to OrganisationGroup, but I think that's a bit too far for my purposes at present.

Remember too that any uncreated group like "[org]_clinicans" should/will be overridden by the default permission set from group name "default_clinicians" if "[org]_clinicians" doesn't exist. This lets orgs override by defining a group with more restrictive permissions if they want, but falls back if that group isn't found to the default permissions for that group.

Actually, is this correct? UPDATE: no - there must be a record in OrganisationGroup for it to match on a User's org-dependent group relational table record. So, no need to create links in the OrganisationGroup table to default groups, but maybe can insert default groups there based on the default group permissions? So basically, when an Organisation is created, for all default groups, create new groups called "[org]_[group]" that carry over all default group permissions.

So:
- Role roughly matches to Group and OrganisationGroup
- Policy roughly matches to permissions as defined/enumerated in models and enforced by services and views that consult OrganisationGroup via the custom BaseBackend


-----------------------

currently, auth works like this:

- the User model has bullshit like:
   - can_administer_system()
   - can_assign_referral_within_phn()
... which depend on the organisation in a local context (action)

- the "active" organisation is derived from the "current_organisation_id" in the session object I think (app/auth/forms.py)
  - the auth user object has like, user.organisations and user.currentorganisation

The flow:
  - who dat user
  - which org is currently selected
  - what roles does user have in org

- Org policies are loaded as a rules engine
  - the AccessPolicy object for the active org is used for:
    - resource is visible
    - action is allowed
    - which roles can do it
... so, load active org policies, map to resources and actions, then see if user has a matching role

So:

1. Get the User
2. Get the active/current Org
3. Load Org Policies
4. Try to match User's Roles against policy/resource/action and allow/deny


Mentioning nothing about the lack of adherence to a pattern (using current_user.is_an_admin_of_some_sort() vs. comparing the user's role list against the org roles and policies), I can see how this might be confusing and inefficient. IIRC we cache the User's permissions but dang.

---------------------------------------------------

In the more elegant solution, I would think that we'd benefit from:
- native Django caching of User permissions and fewer JOINs
- not using complex JSON string parsing to determine allowable user actions
- more expressive/obvious "who has permission to do what" structure (in compact views/models/services)
- It would be more obvious which user groups have which permissions and we can easily resolve these issues in django admin


Still to be figured out:
- how to figure out the current org bits DONE


In the use case "transfer Referral to another Org", wouldn't that just be a User in the owning Org has permission on the view / service "update assigned_org_id or whatever?)

In the situation where a user is a clinical admin in one org and not in the other (and thus should not be able to see the person's name on a Referral), why does it matter what the current org's context is?

Can we just enforce this at the view level by doing a "if user is in a group that allows them to view names on owning org Referrals, let them see the name"? This is weird if the owning org does not want the originating org clinical group members to see the transferred Referral's person's name, or something. But that permission can be resolved in the local views/services context, no? With the permission string being defined on the Referral model?

-----

passing the org context... maybe we can do things like display all referral records for both orgs in the same view for a user that belongs to both? Let's think through CRUD:

- Create: user should select org at create Referral, Contact, etc. time
- Read: The most complex. Possibly resolvable without passing org context by having multiple panes, each corresponding to different orgs. Could be card tabs or separate tables if it is desirable to see all records for all orgs on same page at once
- Update: Generally, don't need org context
- Delete: Generally, don't need org context

with this in mind, do i need org context? Possibly not. Just populate everything based on user's group memberships

might require thinking around AJAX-style stuff as it could be too much querying

At least bootstrap cards are collapsible. Maybe I can have two 100% width cards stacked and rely on the user to hit the minus button if they don't want to see one or the other org

Or put the user in the driver's seat and allow them to choose their own dashboard / interface components?

---------------------------------------------------------------
UI planning:

left hand column items:

(All users)
- Announcements
- People (Consumers)
- Contacts
- Referrals
- Assessments? / Surveys?
- Messages
- Settings
- Help documentation

(Admins of varying kinds)
- Config
  - Users
    - Groups
    - Roles / Permissions (permissions for each org role)
    - Membership (users with associated groups and roles)
  - Templates
- Logs
- Charts
- Reports
- Organisations

on dashboard (might have to make HTMX or separate aggregate table / materialised view / celery-updated task)
- # ContactAttempts for everyone, with change over time
- # Referrals and their statuses, with change over time
- # Assessments for everyone, with change over time
- # IAR-DSTs per person, with change over time
- # ContactRequests this week, with change over time
- ContactRequests - avg. time for returning the call
- Currently available Contacts for ContactRequests (according to their availability)
- Average IAR-DST score over time, per user
- ContactNotes with severity status/alerts(?)
- ReferralEvents / statuses
- Latest Activity
- Latest Messages

Other charts / tables:
- avg age of new Persons
- Consent % for each Consent type
- time spent on contacts over time
- avg time of creation for various models?
- referrals with most frequent updates?
- Survey data


some of these can be in expandable cards so we can HTMX it in via small templates

Interesting - there's a kanban board. im sure that will be useful

Possible that the Projects page could be useful - table with icons for actions

Maybe for charts, so as to not clutter the dashboard, we can put them in a collapsible
card and you can hit expand to see all charts - just display one on the dashboard, or
two side by side

Dashboard:
First, raw numbers in cards in a row:
  - # of incomplete referrals
  - # of incomplete ContactRequests
  - # of incomplete Contacts
  - # of Referrals made this week

Then, "currently available ContactRequests"
  - class="card-body table-responsive p-0"
  - <table class="table table-striped align-middle">...

Then, two charts side by side:
  - Contacts over time by user for the last month
  - ContactRequests over time for the last month

These should be class="apexcharts-canvas apexchartsexagjymm apexcharts-theme-light/dark"
and in DOM divs:
- card
  - row -> col-md-12 -> card-mb-4 -> [card-header -> card-title] /
    [card-body -> row -> col-md-6/col-md-6] -> [card-footer -> row]
  - row -> [4x of:] -> col-md-3 col-6 -> info for footer cards

Then, a list of currently available contacts who haven't been closed?

------------------------

probably allow the user to indicate the referral status manually
  - probably in a different field (user_defined_status?)
  - maybe referral statuses should be able to be definable by the user (admin)?

possibly use the Timeline page (https://adminlte.io/themes/v4/UI/timeline.html) to
show logs for each entity

How to mark ContactRequests as complete? Which statuses make sense? Can reopen?

Perhaps show originating pathway for records related to Referrals/Intake flow (we now
have eReferral/Delta API, CollectAPI, external web form, HealthDirect GP software
integrations which falls under eReferral, etc.)



------------------------

A note on People duplicates:

- it seems impossible to avoid potential Person duplicates according to our business
  logic. Part of this is because we have no guaranteed unique identifier, such as
  Medicare card, especially as we don't have occasion to collect this, or make it a
  necessary field. We also can't expose a Person belonging to one organisation to
  another org unless the user has cross-org permissions to see that data, and/or the
  Person has consented to it,
- three proposed ways to identify potential duplicates (following normalisation like
  to_lower())
  - Levenshtein distance (minimum single character edits to match)
  - Jaccard similarity (word token overlap based on matrices)
  - hash comparison for a composite uniqueness (for speed in checking exact matches)

Maybe this could be implemented in a Celery task that is manually checked periodically
by an org admin of some kind?

-----------------------

Might need to have underlying permissions provisioning after all, or at least some
default permission provisioning up front

permissions should be at model, service, orchestration level, probably not view level

Where to place logic for enforcement of invariants:
- model
  - field constraints, internal validation for state transitions, constraints like
    uniqueness
- single-model services
  - transaction atomicity
  - concurrency control
  - probably de-duping for non-DB constraints, according to business logic?
- orchestration
  - distributed consistency
  - rollback steps (also a kind of atomicity)
  - event ordering


-----------------------

Notes on design by contract
- parse dont validate
- fail fast
- assert result before returning

... I need to move to a statically/strongly typed language

Re: Python type hinting, probably good to have that as a rule

-----------------------

HTMX

debating whether to use django-htmx. leaning against because
- another dependency
- not sure how well maintained
- common usage is in the same views that render the main template, i want custom views
- 

pros of django-htmx:
- no need to check HTMX headers manually, also CSRP
- 

-----------------------

The next things to sort out:

1. Forms / form data flows
2. Needed fields in models
3. Exposing permissions settings to Admins (via Forms)
4. Write the first atomic, permission-specific model-scoped service
5. Write the first orchestration
6. Authentication layer
7. Wire up charts
8. Do HTMX
9. Ninja
10. Multi-tenancy
  - org id on each record? or those records that need it, perhaps?
11. Overlapping Persons (we hide people from search within each org, unless the user has
    cross-org permissions)
  - This could be a service/orchestration level permission, pretty easy I hope

-----------------------

Rich domain model form handling by Gemini:

# forms.py
from django import forms


class PromoteEmployeeForm(forms.Form):
  new_title = forms.CharField(max_length=100)
  effective_date = forms.DateField()


# views.py
from django.shortcuts import render
from mydomain.exceptions import DomainError
from mydomain.services import promote_employee_service


def promote_view(request, employee_id):
  if request.method == 'POST':
    form = PromoteEmployeeForm(request.POST)
    if form.is_dict() if form.is_valid():
      try:
        promote_employee_service(
            employee_id=employee_id, **form.cleaned_data
        )
      except DomainError as e:
        form.add_error(None, str(e))  # Attach domain error to non-field error
      else:
        # redirect on success
        pass
  else:
    form = PromoteEmployeeForm()
  return render(request, 'promote.html', {'form': form})


or rather:

# 1. The Form strictly sanitizes input types
class TransferForm(forms.Form):
    target_account_id = forms.IntegerField()
    amount = forms.DecimalField()

# 2. The View handles HTTP orchestration
class TransferView(FormView):
    def form_valid(self, form):
        # 3. The Rich Domain Model handles the actual business logic
        source_account = self.request.user.account

        try:
            # All business rules live inside this model method
            source_account.transfer_funds(
                target_id=form.cleaned_data['target_account_id'],
                amount=form.cleaned_data['amount']
            )
        except InsufficientFundsError as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)

        return super().form_valid(form)


# A conceptual simplified look at Django's internal FormView logic
class FormView(BaseFormView, TemplateResponseMixin):

    def post(self, request, *args, **kwargs):
        # 1. Django fetches the form class you declared (form_class = TransferForm)
        # 2. It injects request.POST and request.FILES into it automatically
        form = self.get_form()

        # 3. It checks validation
        if form.is_valid():
            # 4. It injects that instantiated form directly into your method!
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class TransferView(FormView):
    form_class = TransferForm  # You declare it here

    # Django injects the instantiated, valid form right here
    def form_valid(self, form):
        # The form is already loaded with data here
        amount = form.cleaned_data['amount']

        # Your domain logic...
        return super().form_valid(form)


class TransferView(FormView):
    form_class = TransferForm
    template_name = 'transfer.html'
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        # Get the default dict (which contains request.POST on a submit)
        kwargs = super().get_form_kwargs()

        # Inject the current user as an extra dependency into the form
        kwargs['user'] = self.request.user
        return kwargs



class TransferForm(forms.Form):
    amount = forms.DecimalField()

    def __init__(self, *args, **kwargs):
        # Pop the injected user out before passing the rest to Django
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

---------------------

next steps:
- set up user/pass auth, template, and routing DONE
- csp package integration (WIP) DONE
- sample htmx workflow
- form page
  - leverage already-installed crispy forms - bootstrap 5

---------------------

Added django-ninja with JWT auth. Send the following JSON via POST:

{
    "email": "derp@derp.com",
    "password": "passssword"
}

Endpoint:

/api/v1/token/pair

...then include Bearer token on each API request.


Pre-flight auth script for Postman to get bearer token:

First, define variables in environment:
- host (127.0.0.1:8005)
- email
- password
- access_token (blank)

const getTokenAuth = {
    url: pm.environment.get("host") + "/api/v1/token/pair",
    method: 'POST',
    header: {
        'Content-Type': 'application/json'
    },
    body: {
        mode: 'raw',
        raw: JSON.stringify({
            "email": pm.environment.get("email"),
            "password": pm.environment.get("password")
        }),
        options: {
            raw: {
                language: 'json'
            }
        }
    }
};

// Send the request
pm.sendRequest(getTokenAuth, (err, res) => {
    if (err) {
        console.log("Auth error:", err);
    } else {
        console.log(res.json());
        const responseJson = res.json();
        const token = responseJson.access;
        console.log(token)
        pm.environment.set("access_token", token);
        console.log(pm.environment.get("access_token"))
        console.log("access_token obtained successfully");
    }
});

# Intake flow at present:
intake flow
- Person calls or callback request received
- Info about Person (if any) is recorded
- Info about the nature of the Service Contact event is recorded
  - possibly outcome, possibly callback availability window
- Info like IAR-DST / Risk assessment data is recorded (if any)
- can convert to Referral if First/Last name, DOB, and pathway/contact type is recorded.
  - NB: DOB can be 9/9/9999 if unknown...
- Referral requires Gender, Postcode, and one of phone or email and contact preference
  - NB: enter 9999 if Postcode is unknown, but "Unknown" if Country of Birth and Main language at home are unknown.
  - some more demographic details here
- Move to Referral page which shows:
  - Referral origin
  - Additional documentation
  - Notes
  - IAR-DST w/ calculated level of care and practitioner assessed Level of Care
  - Risk Assessment
  - Consent fields
  - List additional service providers or whoever that can be contacted
  - Referral outcome(s)
    - Service type, notes, sent status
  - Logs, metadata like UUIDs
- Once certain demographic fields, contact details (e.g. phone number) and consent fields are filled in, can mark "sent" on referral outcome. This "locks" the referral
- On the referral lock screen, the referral date, follow up date, notes, referral outcome including the toggle for "accepted", person's demographics, referrer info, IAR-DST/Risk assessment, and consents
  - this is basically the Client and Referral data combined
  - can mark each referral outcome accepted or not
  - admins can "unlock"
- can print from each page
- print options include toggles for:
  - suicide referral
  - recommended LoC
  - Practitioner Assessed LoC
  - Show legal name (vs. preferred)
- printing a referral has pretty much everything in it
  - displays name according to the permissions (e.g. a clinician can print full name)
  - printing a Contact has pretty much just the info on the Contact modal



My meeting with Steven to do the flowchart and ask a sample permissions issue

v2 Flowchart for PMHCIS app / MMHCI

"Consumer calls"
- add MMHC walk ins
- they can also fill in the form on medicarementalhealth.com.au to get a call back

-> routed to PHN by catchment area based on postcode, shows up as pop up menu on the upper right of PMHCIS app with call back requests


on staging:
every morning, all intake clinician roles are removed


"person just wanted information"
- based on outcome, we make a decision about how to proceed
- group diamond "does consumer want a call back or proceed?" into "staff gather information from Consumer"

We make 3 call back attempts (across all PHNs) before abandoning the contact, if we can't do it, we record the "outcome" as uncontactable or something. It drops off of "incomplete contacts"

rename "Intake" as "Convert"

"Is intake admin a clinician?"
- rename to "if the person managing the client/referral is a clinician"
- no, actually delete this record

- they review the contact, referral, attachment, and note records (CRAN)

- IAR-DST and Risk Assessment both is always completed for the Referral to progress
  - no, actually this depends on the org policy and it relies on the reason being given (the latter "relies on reason given" is ironclad for all PHNs)

- Referral requires Outcome to be recorded before the Referral can be marked Complete

"Should the referral be sent"
- not a conditional, all referrals need action
- they all go to sent or accepted

- intake teams conduct warm handover for complete referrals, where they contact the service providers. this is between when a referral is "complete" and "sent"

- if service provider does not accept, a new one must be found

- "sent_datetime" for referral is the only flag that can prove that the referral was marked sent from the reporting perspective

- service provider lets intake team know when they can take the referral, intake team or our system marks as Accepted

- a referral is marked "locked" when it is sent.

- sent and accepted are in the "Referral Outcome" part of the Referral page.


Permissions issue previously encountered:
- Intake clinician should have been able to accept only
  - but then we figured out that intake admins receive the message that the referral could not be progressed
- so intake clinican or system admin (Caroline's team) needed to be contacted to remove the service provider
- we added a permission to handle this

---------------------------------------------

# Orchestration / applying a services flowchart to track Referral state
It makes sense to use the Orchestration Pattern to manage the preparation
and state of a Referral, similar to a Finite State Machine. This is one way
of writing tax preparation software.

The Orchestration Pattern is a good idea because it manages a Directed Acyclic
Graph (DAG) that only needs to calculate that portion of the workflow after
the current stage, rather than recalculating the graph every time something
changes. FSMs also tend to grow in complexity and need to be redefined in a
much more clunky and side-effect causing way, IMO.

It also can manage more complex state transitions, external dependencies, and
background tasks more elegantly than a model-driven FSM can. It fits well
with the Model -> Service -> Orchestration pattern I have implemented so far
in this app.

It would be nice for admins/clinicians to come back to any incomplete contact
or referral and know exactly where in the stage things are, instead of having
two tabs / no centralised mechanism. It would seem to me that the state and
required fields before proceeding to the next step would be more intuitive
in this way.

I worry about team understanding of the workflow, but maybe this is easier in
the long run vs. having a more atomised and hidden / emergent state.

This would involve the following components:

- A Context object - the class representing the data of the Intake
  workflow (e.g. class "IntakeContext" with fields like
  "PersonConsent.collect_data"). This might be implemented as an object which
  contains many FK references to the Referral/Consent/etc. tables. The
  IntakeOrchestrator task evaluates the Context object to find the current
  workflow state (see below). The IntakeContext object can also have its
  own state, e.g. "Completed", in case a Task knows that the Intake workflow
  has reached a terminal state, such as when a Person's ContactRequest
  can't be reached after three attempts. The Task would update the
  IntakeContext status to "complete" or similar, so that the Orchestration
  object can pick that up and prevent the calculation of the "next task".
- A BaseTask object for all Task objects, which contains base
  implementations for task name and dependency list variables, and
  a passthrough execute() method
- Task objects that implement execute(), which call services to do whatever
  is needed at that stage (e.g. validate all required information exists in
  the Referral object before the Referral can be marked "Sent"). The Task
  objects would save information back to the Context object. Each Task may
  have a "state" like "in progress", "complete", "not started", etc.
- An Orchestration object, say, IntakeOrchestrator, that defines a variable
  "tasks" that is a list of individual Task classes with their task names
  and their respective dependencies (dependencies are lists with the names of other tasks). This object would have a function that returns which tasks
  have been completed and what the next task is.

Calculating where the current state is, in IntakeOrchestrator:
intake_context = IntakeContext(id)
if intake_context.status = "complete"
  return False   // or redirect or whatever.
completed_tasks = task.name
                  for task in intake_workflow.tasks
                  if task.status = "complete"
for task in tasks:
  if task.name in completed_tasks:
    continue
  // (if all tasks are completed, send to final screen)
  next_task = task  // or rather, a list of tasks as some can be parallel

Database tables can be made for the IntakeContext, and IntakeEvents
for storing state, the output of tasks, and for logging/traceability. The
current state of the workflow is found by evaluation of IntakeContext variables within the IntakeOrchestrator class, not by persistence through DB variables in a Task DB table. This means that IntakeContext must have
references to each Task and its state. Otherwise each Task should get its
own DB table and an FK to the task can be saved in the IntakeContext object.

UPDATE: ok, I have decided to create a Task DB table because storing variables
corresponding to Task state within the IntakeContext is not a good idea,
because it risks making a God object of IntakeContext, reduces data
normalisation, and doesn't allow for complex querying. The IntakeContext
model will have a M:M FK association with Tasks. The Task table will store
the name of the task and its state, and possibly other metadata (e.g.
"started_at" and "ended_at" so that "time spent in that state" can be queried).

Need to allow a state option for "skipped" in each Task to allow for
conditional task management. As we are iterating through Tasks in the
workflow, we can skip any individual task dependency this way.

In Django, I need to implement locking for these workflow tasks so as to
prevent race conditions. This would occur during state transitions and any
other needed insert/update/delete operations in the database. This would
involve using .select_for_update() within @transaction.atomic or a context
manager context like "with transaction.atomic():".

IntakeContext is a coordination data structure for everything. Tasks store
references to the records they create/modify in that object. It is a shared
data bus, so if a future task depends on the data created by a prior task,
it can read it from the IntakeContext object reference (e.g. a Referral
might need to be created and do some sort of validation step which references
the previously created PersonAddress).

So, in terms of the UX, there will still be Views for things like "ContactRequest"
and other domain objects, and even an "Incomplete ContactRequest" view etc., but the
main screen will likely be "incomplete IntakeContexts" that are basically a view
of the workflow instead of the records that have "missing" data.

Also, the orchestration will basically be a service that allows the router or a view
to determine the next view to present.

And perhaps each of the workflow views will show which stage the workflow is in via
something like chevrons, and allow editing previous data. Editing a previous record
can maybe unset the "completed" flag on the IntakeContext? There needs to be rollback
handling, possibly a rollback() function in each Task. Need to flesh this out.

--------------------------

Hmm, maybe not orchestrated rollback()s. Maybe dynamically compute the workflow stage every time the page is loaded. It might be too many queries... but simple ones. Simpler than an event-driven architecture, but still performant enough.

So, keeping the workflow orchestration... on the main Intake workflow view:
- re-run each Task to see whether changes were made. Check the Task instance for whether the dependent models were updated since the Task was run, which means comparing the saved Task info to the models referenced by the Task. This may be as simple as 1:M calls to a function that lives in the single-model service to compare the task updated_at with the model's updated_at.
- or, for each Task, e.g. "referral_complete", run Task.is_valid() which queries all dependent models to see whether the Task.updated_at field is older than any of the model updated_at fields. If so, the Task is stale and needs to be reset from state = "completed" and back to "incomplete".

Maybe it is better for the "stale detection" logic to live in the service? Or is it the service that interacts with the model that is better?

Turns out this is a just-in-time (JIT) validity reconciliation model. So I can place an
is_valid() function inside each Task from the BaseTask class, that calls 1:M services'
is_stale() that takes as input a datetime and returns whether the underlying model
instance or instances has (have) a newer datetime. If there are many models to query,
the orchestration (multi-model) service can also implement this same function.

So it looks like, in the IntakeOrchestrator object, as each workflow stage is being
iterated through, the Task's is_valid() function is called, and if that returns False,
the workflow stage is automatically set to the current Task, and the latter tasks are
also state-invalidated? UPDATE: no, actually, because this is re-calculated and self-
healing, state is not tracked. I think?

So essentially, the Tasks have information on the stage of the Intake workflow such as
metadata like "last_calculated" or "executed_by", but the Tasks don't explicitly persist
a "state", because it is continuously re-calculated.

The single-model services have a concept of state local to the single model, but not
the workflow.

Maybe each step can have a UI element that says something like "this step has enough
data to proceed to the next step", i.e., the record has enough mandatory data, but is
available for review and editing.

This is a WIP.

what's the simplest way to write this i wonder

Literally:
def detect_workflow_stage(intake_id):   ## Depends on person_id -> choose Intake?

1. The user searches for the Person and finds the Person view.
2. The user can select any Intake workflow instance (in our current app, this is essentially a Referral/Client record, or a Contact record depending on whether the Person has not ever progressed to that stage).
  - Is the Intake selection based on IntakeContext? Via an IntakeOrchestration method?

or

1. The user doesn't find the Person and starts a new Intake

At any time, the user can go into an individual Referral or whatever record and change it manually. Because the workflow is recalculated each time, don't need to worry about updates.

I wonder, however, if we store something like last_calculated in Tasks, whether that becomes stale when we edit records manually? No, actually no problem there.

Creating an Intake record is tricky.

Could create an Intake at the first Service Contact with a new Person if the Person record is created? Is a Referral record being created a necessary thing? It seems a required field for the creation of an Intake record for reporting purposes. But the start date for an Intake is the time of first Service Contact.

Must also independently support searching for Service Contacts basically by record created - user should be able to search for any previous contact record created by any field that they have access to.

## Possibly useful prod commands (in mmhci dir)

git pull origin main
docker compose -f docker-compose.production.yml build
docker compose -f docker-compose.production.yml up -d postgres redis
docker compose -f docker-compose.production.yml run --rm django python manage.py migrate
docker compose -f docker-compose.production.yml up -d
docker compose -f docker-compose.production.yml run --rm django   python manage.py shell -c   "from django.core.mail import send_mail; print(send_mail('test', 'test', None, ['noreply@githeri.com']))"
docker logs mmhci-traefik-1
docker logs mmhci-django-1
docker compose -f docker-compose.production.yml logs

# django-auditlog for reads/writes in services layer

base service class for auditing

from contextlib import contextmanager
from auditlog.context import set_actor
from auditlog.signals import accessed

class BaseService:
    def __init__(self, request):
        """
        Instantiate the service with the incoming HTTP request.
        This provides clean, persistent access to request.user and request.META.
        """
        self.request = request
        self.user = request.user

    @contextmanager
    def audit_write(self):
        """
        Context manager to safely wrap database write operations.
        Ensures django-auditlog background signals grab the correct user.
        """
        # Checks if user is logged in (handles Django & DRF auth states)
        actor = self.user if self.user and self.user.is_authenticated else None

        with set_actor(actor=actor):
            yield

    def log_access(self, instance):
        """
        Explicitly triggers an access/read log entry for a specific model instance.
        Passing the request automatically fills the actor and remote IP address fields.
        """
        accessed.send(
            sender=instance.__class__,
            instance=instance,
            request=self.request
        )

then, in services:

# myapp/services/document_service.py
from .base import BaseService
from myapp.models import Document

class DocumentService(BaseService):

    def get_document_details(self, document_id):
        """Fetches a document and tracks the read event."""
        document = Document.objects.get(id=document_id)
        
        # Logs the read access to SQL database
        self.log_access(document)

        return document

    def update_document_title(self, document_id, new_title):
        """Updates a document and tracks the modification event."""
        document = Document.objects.get(id=document_id)

        # Automatically ensures user is captured during model updates
        with self.audit_write():
            document.title = new_title
            document.save()

        return document

better safety for audit_write in service base class:

    @contextmanager
    def audit_write(self):
        actor = self.user if self.user and self.user.is_authenticated else None

        # Open the inner layer
        with set_actor(actor=actor):
            try:
                yield  # Hand over control to your database updates
            finally:
                # This block is GUARANTEED to run, even if the database code crashes.
                # It ensures the inner context manager closes cleanly no matter what.
                pass

-----------












































































































































## Standard Cookiecutter-Django README

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Settings

Moved to [settings](https://cookiecutter-django.readthedocs.io/en/latest/1-getting-started/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      uv run python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    uv run mypy mmhci

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    uv run coverage run -m pytest
    uv run coverage html
    uv run open htmlcov/index.html

#### Running tests with pytest

    uv run pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/2-local-development/developing-locally.html#using-webpack-or-gulp).

### Celery

This app comes with Celery.

To run a celery worker:

```bash
cd mmhci
uv run celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

```bash
cd mmhci
uv run celery -A config.celery_app beat
```

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

```bash
cd mmhci
uv run celery -A config.celery_app worker -B -l info
```

### Email Server

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server [Mailpit](https://github.com/axllent/mailpit) with a web interface is available as docker container.

Container mailpit will start automatically when you will run all docker containers.
Please check [cookiecutter-django Docker documentation](https://cookiecutter-django.readthedocs.io/en/latest/2-local-development/developing-locally-docker.html) for more details how to start all containers.

With Mailpit running, to view messages that are sent by your application, open your browser and go to `http://127.0.0.1:8025`

### Sentry

Sentry is an error logging aggregator service. You can sign up for a free account at <https://sentry.io/signup/?code=cookiecutter> or download and host it yourself.
The system is set up with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](https://cookiecutter-django.readthedocs.io/en/latest/3-deployment/deployment-with-docker.html).


## Local development

### Start local docker services
docker compose -f docker-compose.local.yml up

### Run management commands
docker compose -f docker-compose.local.yml run --rm django python manage.py migrate

docker compose -f docker-compose.local.yml run --rm django python manage.py createsuperuser

## Running/stream of consciousness notes on model structure

This has become my running notes, I am moving to README.md and out of the core models.py
for now.

Person
  - uuid (autogenerates)
    // unsure about automatically creating a record as we could
    // have many dupes / inappropriate combining of persons
  - consent.id (FK)
  - first_name
  - middle_name
  - last_name
  - dob
  - email
  - preferred_contact_method (e.g. "email" or "phone")
  - phone_number
  - gender
  - sexual_orientation
  - pronouns
  - sex ("Intersex"?)
  - aboriginal_torres_straight_islander
  - country_of_birth
  - main_language_at_home
  - english_proficiency
  - interpreter_required
  - address.id (FK)
  - availability_for_callback // ("Contact timing preference" in current Contact schema)
  - emergency_contact_first_name
  - emergency_contact_last_name
  - emergency_contact_phone_number
  - emergency_contact_relationship_to_client

Contact
  - uuid (autogenerates)
  - person.id (FK)
  - duration
  - pathway
  - contact_category ("contact type")
  - purpose
  - outcome
  - created_by (FK -> User.id)
  - organisation.id (FK)
    // (Is this the org that owns the contact? Field shows if user is
    //  assigned multiple orgs? Seems like it says "current
    //  referral owner" on the referral screen)
  ////////
  // Client fields on next page (after "Conversion") are
  // (should be) in Person, not Referral
  ////////

Address
  - street_address_line_1
  - street_address_line_2
  - street_address_line_3
  - suburb
  - state
  - postcode

Referral
  - uuid (autogenerates)
  - contact.id (FK)
  - pathway
   // (FK to Contact.pathway? Prob not. Called "origin" in Contact at present...
   // keep separate text field? This might need to be edited separately)
  - owned_by_organisation (FK) (Organisation.id)
  - homelessness
  - income_source
  - labour_force_status
  - employment
  - health_care_card
  - ndis
  - marital_status
  - reason_created
  - iar_skipped
    //(I have seen us apply different logic for
    // null and "N/A" or "skipped" meaning on purpose)
  - reason_iar_skipped
  - iar_dst_referral (FK) (nullable)
  - practitioner_assessed_level_of_care
  - practitioner_reason_level_of_care
  - risk_assessment.id (FK)
  - risk_assessment_skipped (nullable)
  - reason_risk_assessment_skipped
  // TODO: many dependent fields and many possible outcomes here,
  // prob. need to make relational table(s).
  // Also, the ReferredTo table has a referral_outcome field.
  // I think refactor into a relational table and an Outcome table
  - referral_outcome.id (FK)
  - gp_feedback_sent
  - gp_feedback_sent_at
  - referrer_feedback_sent
  - referrer_feedback_sent_at
  - follow_up_incomplete
  - follow_up_due
  - completed_by
  - completed_at

Referrer
  - organisation.id (FK, nullable)
  - profession
  - type
  - name
  - phone_number
  - fax_number
  - email

IarDstVersion
  - name
  - description
  - developmental_age_group

IarDstItem
  - name
  - description
  - scoring_description
  - iar_version.id (FK)

IarDstAnswerChoice
  - score (severity)
  - iar_dst_item.id (FK)

RiskAssessment
  - referral.id (FK)
  - suicide_thoughts
  - suicide_plan
  - suicide_intent
  - suicide_attempt_3_months
  - suicide_risk_level
  - suicide_referral
  - suicide_note
  - self_harm_thoughts
  - self_harm_plan
  - self_harm_intent
  - self_harm_behaviours
  - self_harm_risk_level
  - self_harm_note
  - others_harm_thoughts
  - others_harm_plan
  - others_harm_intent
  - others_harm_risk_level
  - others_harm_note
  - harm_from_others_risk
  - harm_from_others_note

// TODO: think about changing this to more of a relational table structure... not great.
// Or, move it into the respective tables. And maybe FK the consent table from
// the FK tables
Consent
  - person.id (FK, nullable)
  - contact.id (FK, nullable)
  - referral.id (FK, nullable)
  - receive_service_info_and_sharing
  - share_de_id_data_with_dohda
  - survey
  - contact_members_of_care_team
  - care_team_note
  - consent_voice_message
  - consent_sms

ReferralOutcome ("ReferredTo"?)
  - referral.id (FK)
  - name
  - description
  - service_type  // some of these have an option for org id
  - service_provider (FK, org.id. Nullable.)
  - service_provider_type  // if service_provider is "Other", might be a lookup table
  - sent_at
  - accepted // This field captures both null and false values - different meanings
  - accepted_at
  // Need to document abandon_reason if abandoned
  - note

Tag
  - name
  - description

// A note on org policies: looks like it's currently like: enter policy name and
// description, select a resource (not sure how options are populated but they don't
// appear to be manually added to the list. Is there a query to get what fields
// are available?) - example: "Contact.legacy_notes_field [display]". UPDATE: looks
// like they come from forms.py in the h2h repo.
// Then select Permitted Roles (is this different per org?), then toggle "Allow"
// and hit Save (is "Allow" toggle really necessary?)
// https://pmhcis-staging.intake.org.au/manage_organisation_policy

Policy
  - name
  - description
  - rules? (JSON? Might need to add a good amount of logic) (see above note)
Organisation
  - name
  - name_alternative
  - short_name
  - description
  - phone_number
  - phone_number_alternative
  - state
  - organisation_group (FK? string?)
  - organisation_path (e.g. "PHN201:PHN201")
  - is_phn
  - is_site
  - is_removed (change to "active" bool?)
  - mmh_callback_requests_activated
  - follow_up_days_default (move to org policies / settings table?)
User (provided by cookiecutter, but add fields)
  - last_seen
  - last_deactivated(?)
  - deactivated
  - deactivated_at
  - deactivated_reason
  - deactivated_by
  - active
  // If not provided by the User model extension from cookiecutter:
  - created_by
  - updated_by
  - created_at
  - updated_at
Role
  - name
  - description

// TODO: consider the log table (DynamoDB? Put all in one place?
// Keep relational? Keep in the same DB? CQRS in read only replica?)
Log
  - event info (JSONB?) or:
  - event (verb to describe act, e.g. "viewed", "added")
  - by_user (FK to User.id)
  - ip_address
// Need to sort out CallBack, CallBackRequest, CallBackAttempt and prob.
// relational tables
CallBackRequest
  - not sure if this should be a separate table or a field in contact
Quiz
  - (IAR-DST fields defined in spec)
  - name
  - description
  - quiztemplate.id (FK)
Note
  - text
  - created_by
FileUpload
  - location_on_disk
  - referral.id (FK)

Relational tables:
IarDstReferral
  - iar_dst_version.id (FK)
  - referral.id (FK)
  - recommended_level_of_care
  - note
IarDstItemResult
  - iar_dst_referral.id (FK)
  - iar_dst_item.id (FK)
  - iar_dst_answer_choice.id (FK)
  - note
IarDstTemplate
  - name
  - description
  - organisation (FK)
  - shared
IarDstTemplateField
  - name
  - iar_dst_template (FK)
  - iar_dst_item (FK)
  - text
UserRole
  - user.id (FK)
  - role.id (FK)
UserOrganisationRole
  - user.id (FK)
  - role.id (FK)
  - org.id (FK)
OrganisationPolicy
  - org.id (FK)
  - policy.id (FK)
OrganisationUser
  - organisation.id (FK)
  - user.id (FK)
OrganisationRole
  - organisation.id (FK)
  - role.id (FK)
OrganisationRolePolicy
  - organisation.id (FK)
  - organisationrole.id (FK)
  - organisationpolicy.id (FK)
  - active
ContactQuiz
  - contact.id (FK)
  - quiz.id (FK)
PersonContact
  - person.id (FK)
  - contact.id (FK)
PersonAddress
  - person.id (FK)
  - address.id (FK)
ReferralTag
  - referral.id (FK)
  - tag.id (FK)
  - added_by_user (FK) (user.id)
// Note that there seem to be two different styles of notes in the Referral flow:
// One is pre-completion and a single text field (I think)
// After, a user can add an arbitrary number of notes
ReferralNote
  - referral.id (FK)
  - note.id (FK)

Lookup tables:
QuizTemplate
  - quiz.id (FK)
  - template.id (FK)
...many others to be added here, e.g. UserIarDstTemplate.

--------------------------------------------
Alternate strategy:

Core models

Log (needed for reads/views as they are not supported by native Django logging)
  - text (JSONB?)
Address
  - address1
  - address2
  - address3
  - suburb
  - state
  - postcode
Announcement
  - needed for flash messages
Assessment
  - type (IAR-DST or Risk Assessment)
  - version
Person
  - needed for personal details. Demographics, phone?, email?, pronouns?
  - Need to sort out changes over time to the latter 3
  - also need next of kin / carer details
PersonAddress
  - person (FK)
  - address (FK)
  - is_active (move this to a PersonAuditLog table?)
PersonAuditLog
  - records changes to demographic info over time (latest is stored in Person table)
Consent
  - structure incl. all consent types/fields/elements globally
ConsentNote
  - relational table
Contact
  - needed for:
    - datetime of call
    - time spent
    - call type
    - assigned/initiated org
    - pathway
    - outcome
  - calculated field slk
ContactAttempt
  - relational table
  - capture events like SMS/email sent, tried to call at
ContactConsent
  - relational table
ContactNote
  - relational table
ContactPerson
  - relational table
ContactUpload
  - relational table
ContactRequest
  - needed to record if/when the person needs to be contacted again, and what way
  - also need a reference to quiz data record?
  - status
Note
  - text of note
Referral
  - originating entity
  - person (FK)
  - org_initiated (FK)
  - org_assigned (FK)
  - follow up date
  - iar_dst_skipped
ReferralConsent
  - relational table
ReferralStatus
  - lookup table
ReferralAuditLog
  - records changes to referral data (e.g. status) over time (latest is stored in
Referral)
ReferralUpload
  - relational table
Organisation
  - name
  - name_alt
  - name_abbreviated
  - code (as in phn code / organisation path)
  - is_phn
  - phn (recursive FK, nullable)
  - is_hub
  - type
  - phone
  - phone_alt
  - logo_filepath
  - provider_type
OrganisationAddress
  - organisation (FK)
  - address (FK)
Outcome
  - Referral sent and accepted information, like datetimes?
  - which Service referred to (generally, a site)
Policy
  - name
  - description
OrgPolicy
  - org (FK)
  - policy (FK)
  - resource (FK) (nullable)
Role
  - name
  - description
OrgRolePolicy (supersedes OrgPolicy)
  - org (FK)
  - role (FK)
  - policy (FK)
  - resource (nullable) (FK)
Resource (for defining access in policies)
  - name
  - description
ServiceType
  - lookup table
  - (site, containing generic entries like 000, MMHCI, area mental health service etc.)
ReferralOutcome
  - relational table
  - abandoned at datetime
  - sent datetime
  - accepted datetime
ReferralOutcomeNote
  - relational table
ReferralUpload
  - relational table
ReferralNote
  - relational table
RiskAssessment
  - store structure of items, like suicide flag, harm to others, etc.
Role
  - name
  - description
Survey
  - structure of survey data collected, might want to use JSONB
UserOrgRole
  - user (FK)
  - org (FK)
  - role (FK)
Upload
  - string with s3 path

-------------------

Assessment (Risk and IAR-DST) submodule

Assessment
  - referral (FK)
  - assessmenttype (FK)

AssessmentType
  - name
  - version

Measurement
  - measurementitem (FK)
  - value_string
  - value_integer
  - value_number
  - value_boolean
  - value_text (lean away from JSONB)
  - note

MeasurementItem
  - name
  - version
  - meta_name (primary vs. contextual domain)
  - data_type (bool, string, datetime etc) - field itself is string type

AssessmentTypeMeasurementItem (relational, associates assessments with their
measurements)
  - assessmenttype (FK)
  - measurementitem (FK)

AssessmentMeasurement
  - assessment (FK)
  - measurement (FK)

---------------
Templates submodule

There are templates for iar-dst note text, SMS messages, and many other note types, so
maybe it's best to have it be generalisable. It seems that they are not limited by
role/user. They can optionally be shared with other orgs.

Template
  - organisation (nullable) (FK)
  - name
  - shared (bool)

TemplateItem
  - template (FK)
  - name
  - text

...prob some relational tables for templates:

MeasurementItemTemplateItem
  - measurementitem (FK)
  - templateitem (FK)

.....I don't know, maybe come back to this. Maybe this can be denormalised.


---------

SMS submodule

Sms
  - text
  - status
  - category ("follow up"?)
  - sent_datetime (use created_at?)

SmsTemplate
  - name
  - description
  - text
  - trigger_condition (maybe change this later? we don't seem to have more than one per
template)

SmsConsent (move this back into Contact and/or Referral?)
  - person (FK)
  - consent (FK)


We store SMS sending info in the Referral table; might not be ideal. We store SMS
trigger events in the ref_sms_trigger table (not lkup_...)

---------------

Survey submodule

Survey
  - referral (FK)
  - person (nullable) (FK)
  - submitted_datetime (if different from created_at auto-field)
  - [all survey measures, probably version/template/split by item]

...getting fatigued, probably resume later.

-------------------

Core models
  - Consent
  - Address
  - Note
  - Announcement
  - Policy
  - Upload
  - Lookup tables maybe? Prob colocate with their other apps

--------------------


Finding seams / underlying data model in MMHCI and PMHC-MDS reporting

The PMHC-MDS dataset is for reporting, not the same as the data collection web app we run (PMHCIS)

Those that seem essential / map to PMHC-MDS:
- Client - this is the Patient
- Organisation
- Contact ("Service Contact" in PMHC-MDS) - this is more of an event than a person


Entities in PMHC-MDS that don't have a corresponding representation in our code:
- Intake (kinda, we infer it through the state of a Referral... I think)
- IAR-DAT Measure (stupid name, should be iat_dst_intake_exam or similar)
- Collection Occasion
- K10+, K5, SDQ quesionnaire tables
- Service Contact (similar to Contact but not the same)
- Practitioner (similar to Referrer/ReferredTo, but also Organisation)

Entities in h2h that have no representation in PMHC-MDS:
- Referral (closest to Intake)
- Policy
- Role
- CallbackRequest
- [various log/auth/metadata (notes)/custom template/announcement/address/lookup tables/enum tables]

New entities I am suggesting:
- Quiz/QuizTemplate?


Functions present in our PMHCIS app that don't map to PMHC-MDS (prob. non-exhaustive)
- A unified search bar for Contacts/Clients|Referrals by name, initials, phone, DOB
- Create New Contact/Client|Referral
- View incomplete Contact/Client|Referral
- Assign owning org to Referral
- Assign permissions/RBAC/org to user/org/role/policy
  - this can override default permissions "policy" for each role pertaining to a resource in an org
- View Reports -> Contacts
  - input pathways, PII, outcome, created_by, assigned to org, minutes spent
- View Reports -> Referrals
  - last updated/dates, status, pathway, suburb, IAR-DST results, suicide flag, notes, assigned to org/user, input pathway, outcome, PHN if org not PHN, time spent, hours spent
- View Reports -> Abandoned Referrals
  - date, status, pathway, IAR-DST level, abandon reason, notes, org, created_by, hours spent
- View Reports -> "Callback Requests"
  - contact outcomes and pathways
  - contact outcome by PHN and pathway
  - outcomes of "converted callbacks"
    - (when Contacts get a Referral [and are "converted" to a Client], they will/may have a Referral outcome)
- "Inbox" with "Incoming Referrals"
  - this seems to be a sort of staging area. We expose an interface for clients to use an API (Delta API?) to send us data for merging into our system; this seems also to accept the input of the external-facing web form that we host in a different location. The user can review and import each record ("convert to a Referral" -> not the same as converting a Contact/Client to a Referral within this internal web app though)
  - Each Referral ("eReferral" in our language for this staging area) has:
    - a status like converting/converted/new/declined
    - A source
    - date
    - name/DOB
    - suburb, suicide flag, IAR-DST level of care, referrer, assigned to
    - Things like Medicare card / NDIS data
    - IAR-DST data, risk assessment data
    - metadata like notes
    - Attachments associated with the eReferral
    - "Activities", a really good log of what was done, by whom, and when (this is in our fat JavaScript on the Client side, which I would like to move into the server side)
- Dashboards -> Survey: charts based on patient-facing survey data (I felt listened to, overall experience likert measures, etc.)
  - Overall experience likert chart
  - experience over time likert chart
  - chart of positive feedback over time, filterable by date line chart
  - survey responses/% responded vs. time for PHN vs. national rate
- Dashboards -> Intake: charts based on activity by team member and filterable by date
  - Contacts created vs. time (aggregate among all team members or individual)
  - IAR-DSTs completed
  - Average assessment levels by domain (cool!)
  - Team member activity (does not seem implemented?), probably based on ActivityLog
- Ability to download PMHC-MDS data Intake in ZIP file format
- Ability to upload PMHC-MDS data in ZIP file format
- Ability to upload (I think these are rarely used):
  - Service model PDF file(?)
  - System & Telephony Support Process PDF(?)
  - Intake Survey Information PDF
  - Protecting PII in the PMHCIS Intake Module PDF
  - Offline Form Word file
  - Operations Manual PDF
- Ability to specify IAR-DST, Note, and SMS templates (with templates and a "mark as shared")
- A Client and Referral data quality check page (e.g. Records with missing data)
- A user account audit page, listing user activity:
  - User name
  - orgs
  - roles
  - records viewed per month
- A Tag entity system with CRUD
- Print a referral w/ obscured lines if user has no access to PII. Same for Contacts
- Links to various documentation/guides, most notably our help page/documentation which ships with the app
  - https://pmhcis-test.intake.org.au/help
- Basically all the rest, from what I can see, is admin stuff - create new org, assign to org, download list of orgs, upload list of orgs by CSV, edit user details like name, MFA toggle, change password, roles/org level permissions on CRUD operations, etc.
