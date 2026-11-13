from django.urls import path
from .views import DashboardRedirectView, OwnerDashboardView, CashierDashboardView

urlpatterns = [
    path("", DashboardRedirectView.as_view(), name="dashboard"),
    path("owner/", OwnerDashboardView.as_view(), name="owner_dashboard"),
    path("cashier/", CashierDashboardView.as_view(), name="cashier_dashboard"),
]