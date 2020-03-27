import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

phone_number_regex = RegexValidator(
    regex=r"^((\+91|91|0)[\- ]{0,1})?[456789]\d{9}$",
    message="Please Enter 10/11 digit mobile number or landline as 0<std code><phone number>",
    code="invalid_mobile",
)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=14, validators=[phone_number_regex], blank=False, null=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class HospitalProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name="hospital_profile")
    name = models.CharField(max_length=30, null=False)
    gstin = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=100, null=False)


class VendorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name="vendor_profile")
    name = models.CharField(max_length=30, null=False)
    gstin = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=100, null=False)
