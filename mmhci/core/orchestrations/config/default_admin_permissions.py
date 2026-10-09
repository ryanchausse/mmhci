# This data structure is used for provisioning a new org. Defines
# models with an associated permission exclusion list. Used to define
# permissions for a new Admin role associated with the new org. All
# permissions are intended to be gated by the current org id and user
# permissions. This could also be used to give a default permission set
# for the "Add Org Role" page. Will restrict "Add Org Role" to org admins
# or Admins Org Group members only.

default_admin_role_permissions = {
    "auditlog.logentry": ["create_logentry", "change_logentry", "delete_logentry"],
    "core.address": None,
    "core.announcement": None,
    "core.assessmentmeasurement": None,
    "core.assessmentreferral": None,
    "core.assessmenttype": None,
    "core.assessmenttypemeasurementtype": None,
    "core.consent": None,
    "core.contact": None,
    "core.contactattempt": None,
    "core.contactconsent": None,
    "core.contactnote": None,
    "core.contactperson": None,
    "core.contactrequest": None,
    "core.contactupload": None,
    "core.formtemplate": None,
    "core.measurement": None,
    "core.measurementtype": None,
    "core.note": None,
    "core.organisation": ["create_organisation", "delete_organisation"],
    "core.organisationaddress": None,
    "core.organisationformtemplate": None,
    "core.organisationgroup": None,
    "core.organisationgroupmembership": None,
    "core.organisationrole": None,
    "core.person": None,
    "core.personaddress": None,
    "core.personavailability": None,
    "core.practitioner": None,
    "core.practitioneraddress": None,
    "core.practitionerorganisation": None,
    "core.referral": None,
    "core.referralconsent": None,
    "core.referralevent": ["change_referralevent", "delete_referralevent"],
    "core.referralupload": None,
    "core.sms": None,
    "core.smsevent": ["change_smsevent", "delete_smsevent"],
    "core.smsformtemplate": None,
    "core.survey": None,
    "core.tag": None,
    "core.upload": None,
    "core.users": None,
}
