from django.contrib import admin
from django.db import models
from django.urls import reverse


# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    PRODUCT_CATEGORIES = [
        ("ELEC", "Electronics"),
        ("CHEM", "Household chemistry"),
        ("COSM", "Cosmetics"),
        ("AUTO", "Auto goods"),
    ]
    name = models.CharField(max_length=4, choices=PRODUCT_CATEGORIES, unique=True)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=20)
    specialization = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    city = models.OneToOneField(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=20)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Customer(models.Model):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    goods = models.ManyToManyField(Product)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Person(models.Model):
    first_name = models.CharField(max_length=20, null=False)
    last_name = models.CharField(max_length=20, null=False)
    email = models.EmailField(verbose_name='E-mail')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        """
        Returns the url to access a particular person instance.
        """
        return reverse('catalog:person-detail', args=[str(self.id)])


class LogModel(models.Model):
    path = models.CharField(max_length=200)
    METHODS_CHOICES = [
        ("GET", "GET"),
        ("POST", "POST"),
    ]
    method = models.CharField(max_length=4, choices=METHODS_CHOICES)
    STATUS_CODES = [
        (200, "OK"),
        (301, "Moved Permanently"),
        (302, "Found"),
        (304, "Not Modified"),
        (400, "Bad Request"),
        (401, "Unauthorized"),
        (403, "Forbidden"),
        (404, "Not Found"),
        (405, "Method Not Allowed"),
        (406, "Not Acceptable"),
        (500, "Internal Server Error"),
        (501, "Not Implemented"),
        (502, "Bad Gateway"),
        (503, "Service Unavailable"),
        (504, "Gateway Timeout"),
    ]
    status = models.SmallIntegerField(choices=STATUS_CODES)
    query_get = models.JSONField(verbose_name="Query params")
    body_post = models.JSONField(verbose_name="Body params")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.path} * {self.method} * {self.status} * {self.timestamp}"

    @admin.display(boolean=True, description="Query")
    def has_query(self):
        return bool(self.query_get)

    @admin.display(boolean=True, description="Body")
    def has_body(self):
        return bool(self.body_post)
