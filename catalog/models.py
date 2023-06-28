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
