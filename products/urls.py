from django.urls import path

from . import views

urlpatterns = [
    path("", views.ProductListView.as_view(), name="product_list"),
    path("add/", views.ProductCreateView.as_view(), name="product_add"),
    path("<int:pk>/edit/", views.ProductUpdateView.as_view(), name="product_edit"),
    path("<int:pk>/delete/", views.ProductDeleteView.as_view(), name="product_delete"),
    path("categories/", views.CategoryListView.as_view(), name="category_list"),
    path("categories/add/", views.CategoryCreateView.as_view(), name="category_add"),
    path("categories/<int:pk>/edit/", views.CategoryUpdateView.as_view(), name="category_edit"),
    path("categories/<int:pk>/delete/", views.CategoryDeleteView.as_view(), name="category_delete"),
]