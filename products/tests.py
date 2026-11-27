from django.test import TestCase
from django.urls import reverse

from accounts.models import CustomUser
from .models import Category, Product


class ProductTests(TestCase):
    def setUp(self):
        self.owner = CustomUser.objects.create_user(
            "owner1", "o@x.com", "Pass12345!", role=CustomUser.Role.OWNER)
        self.cashier = CustomUser.objects.create_user(
            "cash1", "c@x.com", "Pass12345!", role=CustomUser.Role.CASHIER)
        self.cat = Category.objects.create(name="Food")
        self.product = Product.objects.create(
            name="Siomai", category=self.cat, price="15.00",
            quantity=10, created_by=self.owner)

    def login(self, user):
        self.client.login(username=user, password="Pass12345!")

    def data(self, **kw):
        d = {"name": "Noodles", "category": self.cat.pk, "price": "20.00", "quantity": 5}
        d.update(kw)
        return d

    def test_product_list_requires_login(self):
        r = self.client.get(reverse("product_list"))
        self.assertEqual(r.status_code, 302)
        self.assertIn("/accounts/login/", r.url)

    def test_create_product_valid(self):
        self.login("owner1")
        r = self.client.post(reverse("product_add"), self.data())
        self.assertEqual(r.status_code, 302)
        self.assertEqual(Product.objects.count(), 2)

    def test_create_product_zero_price_rejected(self):
        self.login("owner1")
        r = self.client.post(reverse("product_add"), self.data(price="0"))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Product.objects.count(), 1)

    def test_create_product_negative_quantity_rejected(self):
        self.login("owner1")
        r = self.client.post(reverse("product_add"), self.data(quantity=-1))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Product.objects.count(), 1)

    def test_cashier_cannot_add_product(self):
        self.login("cash1")
        r = self.client.post(reverse("product_add"), self.data())
        self.assertEqual(r.status_code, 403)
        self.assertEqual(Product.objects.count(), 1)

    def test_cashier_cannot_delete_product_by_id(self):
        self.login("cash1")
        r = self.client.post(reverse("product_delete", args=[self.product.pk]))
        self.assertEqual(r.status_code, 403)
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())

    def test_missing_product_returns_404(self):
        self.login("owner1")
        r = self.client.get(reverse("product_edit", args=[9999]))
        self.assertEqual(r.status_code, 404)

    def test_duplicate_category_name_rejected(self):
        self.login("owner1")
        r = self.client.post(reverse("category_add"), {"name": "food"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Category.objects.count(), 1)

    def test_category_with_products_cannot_be_deleted(self):
        self.login("owner1")
        self.client.post(reverse("category_delete", args=[self.cat.pk]))
        self.assertTrue(Category.objects.filter(pk=self.cat.pk).exists())

    def test_cashier_can_view_product_list(self):
        self.login("cash1")
        r = self.client.get(reverse("product_list"))
        self.assertEqual(r.status_code, 200)