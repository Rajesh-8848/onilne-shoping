from django.contrib import admin
from .models import Cat, Products,cart

# Register your models here.
class CatAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug']

admin.site.register(Cat, CatAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display=['name','slug','old_price','price','stock','img']
    list_editable=['price','img']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Products, ProductAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display=['user','name','quantity','price','total_price','image','created_at']


admin.site.register(cart, CartAdmin)