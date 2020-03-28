from django.contrib import admin

from .models import Category, Item, Requirement

# Register your models here.
admin.site.register(Item)
admin.site.register(Requirement)
admin.site.register(Category)
