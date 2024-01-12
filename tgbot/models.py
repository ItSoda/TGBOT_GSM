from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self) -> str:
        return f"{self.name}"


class Brand(models.Model):
    name = models.CharField(max_length=150)
    category = models.ManyToManyField(Category, related_name="brands")

    def __str__(self) -> str:
        return f"{self.name}"


class Product(models.Model):
    name = models.TextField()
    price = models.BigIntegerField(default=0)
    currency = models.CharField(max_length=100, default="₽")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name} | {self.category} | {self.brand}"


class Admin(models.Model):
    UUID = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.UUID}"
