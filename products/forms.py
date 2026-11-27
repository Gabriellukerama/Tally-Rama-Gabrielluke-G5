from django import forms

from .models import Category, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if Category.objects.filter(name__iexact=name).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A category with this name already exists.")
        return name


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("name", "category", "price", "quantity")