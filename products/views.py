from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from accounts.mixins import OwnerRequiredMixin
from .forms import CategoryForm, ProductForm
from .models import Category, Product


# ---------- Products ----------

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        qs = Product.objects.select_related("category")
        category = self.request.GET.get("category", "")
        if category.isdigit():
            qs = qs.filter(category_id=category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["selected"] = self.request.GET.get("category", "")
        return context


class ProductCreateView(OwnerRequiredMixin, SuccessMessageMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/form.html"
    success_url = reverse_lazy("product_list")
    success_message = "Product added."
    extra_context = {"title": "Add product", "cancel_url": reverse_lazy("product_list")}

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductUpdateView(OwnerRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "products/form.html"
    success_url = reverse_lazy("product_list")
    success_message = "Product updated."
    extra_context = {"title": "Edit product", "cancel_url": reverse_lazy("product_list")}


class SafeDeleteView(OwnerRequiredMixin, DeleteView):
    """Delete, but show a friendly error if other records still depend on it."""
    template_name = "products/confirm_delete.html"
    success_message = "Deleted."
    protected_message = "This record is still in use and cannot be deleted."

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
        except ProtectedError:
            messages.error(self.request, self.protected_message)
            return redirect(self.success_url)
        messages.success(self.request, self.success_message)
        return response


class ProductDeleteView(SafeDeleteView):
    model = Product
    success_url = reverse_lazy("product_list")
    success_message = "Product deleted."
    protected_message = "This product is part of recorded sales and cannot be deleted."
    extra_context = {"cancel_url": reverse_lazy("product_list")}


# ---------- Categories ----------

class CategoryListView(OwnerRequiredMixin, ListView):
    template_name = "products/category_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.annotate(num_products=Count("products"))


class CategoryCreateView(OwnerRequiredMixin, SuccessMessageMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "products/form.html"
    success_url = reverse_lazy("category_list")
    success_message = "Category added."
    extra_context = {"title": "Add category", "cancel_url": reverse_lazy("category_list")}


class CategoryUpdateView(OwnerRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "products/form.html"
    success_url = reverse_lazy("category_list")
    success_message = "Category updated."
    extra_context = {"title": "Edit category", "cancel_url": reverse_lazy("category_list")}


class CategoryDeleteView(SafeDeleteView):
    model = Category
    success_url = reverse_lazy("category_list")
    success_message = "Category deleted."
    protected_message = "This category still has products. Move or delete them first."
    extra_context = {"cancel_url": reverse_lazy("category_list")}