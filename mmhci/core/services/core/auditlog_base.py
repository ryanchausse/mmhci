from contextlib import contextmanager
from auditlog.context import set_actor
from auditlog.signals import accessed


class AuditLogBaseService:
    def __init__(self, request):
        self.request = request
        self.user = request.user

    @contextmanager
    def audit_write(self):
        actor = self.user if self.user and self.user.is_authenticated else None

        with set_actor(actor=actor):
            # To handle context cleanup for potential crashes in the service layer
            try:
                yield
            finally:
                pass 

    def log_access(self, instance):
        accessed.send(
            sender=instance.__class__,
            instance=instance,
            request=self.request
        )
