from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View


class ChangeCurrentOrgView(View):
    def post(self, request):
        new_current_org_id = int(request.POST.get("new_current_org_id"))
        if new_current_org_id and request.org_perms.get(new_current_org_id):
            request.session["current_org_id"] = new_current_org_id
        next_url = request.POST.get("next")
        safe_redirect = url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure()
        )
        if next_url and safe_redirect:
            return redirect(next_url)
        else:
            return redirect('core:dashboard')
