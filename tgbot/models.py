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

from django.db import models


class UserBot(models.Model):
    """БД для хранения данных о пользователях"""

    user_id = models.BigIntegerField(verbose_name="USER ID", unique=True)

    username = models.CharField(max_length=256, null=True, blank=True)

    first_name = models.CharField(
        verbose_name="Name",
        max_length=256,
    )

    last_name = models.CharField(max_length=256, null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "тг_бот"
        verbose_name_plural = "ТГ_БОТ"


class News(models.Model):
    text = models.TextField()
    photo = models.ImageField(upload_to="news_bot_images", null=True, blank=True)

    class Meta:
        verbose_name = "новость"
        verbose_name_plural = "Новости"