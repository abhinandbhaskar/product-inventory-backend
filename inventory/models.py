import uuid
from django.utils.translation import gettext_lazy as _
from versatileimagefield.fields import VersatileImageField
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    


class Products(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ProductID = models.BigIntegerField(unique=True)
    ProductCode = models.CharField(max_length=255, unique=True)
    ProductName = models.CharField(max_length=255)
    ProductImage = VersatileImageField(upload_to="uploads/", blank=True, null=True)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UpdatedDate = models.DateTimeField(blank=True, null=True)
    CreatedUser = models.ForeignKey("auth.User", related_name="user%(class)s_objects", on_delete=models.CASCADE)
    IsFavourite = models.BooleanField(default=False)
    Active = models.BooleanField(default=True)
    HSNCode = models.CharField(max_length=255, blank=True, null=True)
    TotalStock = models.DecimalField(default=0.00, max_digits=20, decimal_places=8, blank=True, null=True)

    class Meta:
        db_table = "products_product"
        verbose_name = _("product")
        verbose_name_plural = _("products")
        unique_together = (("ProductCode", "ProductID"),)
        ordering = ("-CreatedDate", "ProductID")





class Variant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)  # e.g., Size, Color

    def __str__(self):
        return self.name



class SubVariant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='options')
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.variant.name}: {self.value}"


class ProductVariantMap(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='variant_mappings')
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('product', 'variant'),)

    def __str__(self):
        return f"{self.product.ProductName} uses {self.variant.name}"


class ProductVariantCombination(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='combinations')
    combination_code = models.CharField(max_length=255, unique=True)  # e.g., SHIRT-M-RED
    subvariants = models.ManyToManyField(SubVariant, related_name='combinations')
    stock = models.DecimalField(default=0.00, max_digits=20, decimal_places=8)

    def __str__(self):
        return f"{self.product.ProductName} - {self.combination_code}"


class StockTransaction(models.Model):
    STOCK_TYPE_CHOICES = (
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_variant = models.ForeignKey(ProductVariantCombination, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=3, choices=STOCK_TYPE_CHOICES)
    quantity = models.DecimalField(max_digits=20, decimal_places=8)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.product_variant.combination_code} - {self.quantity}"