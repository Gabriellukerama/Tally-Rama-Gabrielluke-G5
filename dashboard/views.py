from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView
from accounts.models import CustomUser


class DashboardRedirectView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role == CustomUser.Role.OWNER:
            return redirect("owner_dashboard")
        return redirect("cashier_dashboard")


class OwnerDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "dashboard/owner.html"

    def test_func(self):
        return self.request.user.role == CustomUser.Role.OWNER


class CashierDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "dashboard/cashier.html"

    def test_func(self):
        return self.request.user.role == CustomUser.Role.CASHIER