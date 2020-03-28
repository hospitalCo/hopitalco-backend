import uuid
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
# from rest_framework.authtoken.models import Token
from django.core.validators import RegexValidator

phone_number_regex = RegexValidator(
    regex="^((\+91|91|0)[\- ]{0,1})?[456789]\d{9}$",
    message="Please Enter 10/11 digit mobile number or landline as 0<std code><phone number>",
    code="invalid_mobile",
)

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=14, validators=[phone_number_regex], blank=False, null=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
 
class HospitalProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name='hospital_profile')
    name = models.CharField(max_length=30, null=False)
    gstin = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=100, null=False)
    
    def __str__(self):
        return f'{self.name}'
        
class VendorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='vendor_profile')
    name = models.CharField(max_length=30, null=False)
    gstin = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f'{self.name}'

class Category(models.Model):

    name = models.CharField(max_length=30, null=False)

class Item(models.Model):

    name = models.CharField(max_length=30, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, related_name='item')

    def __str__(self):
        return f'{self.name}'

class Requirement(models.Model):

    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=False, related_name='requirement')
    hospital = models.ForeignKey(HospitalProfile, on_delete=models.CASCADE, null=False, related_name='requirement')
    units = models.CharField(max_length=20, null=True, blank=True)

class Stock(models.Model):

    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=False, related_name='stock')
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, null=False, related_name='stock')
    units = models.CharField(max_length=20, null=True, blank=True)
    