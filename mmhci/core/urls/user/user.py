from django.urls import path

from mmhci.core.views.user import create_user
from mmhci.core.views.user import list_users
from mmhci.core.views.user import view_user
from mmhci.core.views.user import update_user

urlpatterns = [
    path(
        "",
        list_users.ListUsersView.as_view(
            template_name="adminlte_4_1/mmhci/admin/users/list_users.html"
        ),
        name="list",
    ),
    path(
        "<uuid:uuid>/",
        view_user.ViewUserView.as_view(
            template_name="adminlte_4_1/mmhci/admin/users/user_view_or_update.html"
        ),
        name="view",
    ),
    path(
        "<uuid:uuid>/update",
        update_user.UpdateUserView.as_view(
            template_name="adminlte_4_1/mmhci/admin/users/user_view_or_update.html"
        ),
        name="update",
    ),
    path(
        "create",
        create_user.CreateUserFormView.as_view(
            template_name="adminlte_4_1/mmhci/admin/users/user_create.html"
        ),
        name="create",
    ),
]
