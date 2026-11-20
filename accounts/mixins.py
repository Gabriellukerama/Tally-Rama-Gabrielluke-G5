from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import CustomUser


class OwnerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Logged-out users go to login; non-owners get a 403."""

    def test_func(self):
        return self.request.user.role == CustomUser.Role.OWNER