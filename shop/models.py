from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

# Create your models here.
class Cat(models.Model):
    name=models.CharField(max_length=250,unique=True)
    slug=models.SlugField(max_length=250,unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return '{}'.format(self.name)

class Products(models.Model):
    name=models.CharField(max_length=250,unique=True)
    slug=models.SlugField(max_length=250,unique=True)
    img=models.ImageField(upload_to='media')
    desc=models.TextField()
    old_price = models.IntegerField()
    price=models.IntegerField()
    stock=models.IntegerField()
    available=models.BooleanField
    category = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.name)

    def get_url(self):
        return reverse


class cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price=models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='cart_images/', blank=True, null=True)  # Add this line
    created_at = models.DateTimeField(auto_now_add=True)