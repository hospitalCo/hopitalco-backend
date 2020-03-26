import uuid
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.core.validators import RegexValidator

phone_number_regex = RegexValidator(
    regex="^((\+91|91|0)[\- ]{0,1})?[456789]\d{9}$",
    message="Please Enter 10/11 digit mobile number or landline as 0<std code><phone number>",
    code="invalid_mobile",
)

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_hospital = models.BooleanField(default=True)
    name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    phoneNumber = models.CharField(max_length=14, validators=[phone_number_regex])
    def __str__(self):
        return self.username
 
class HospitalProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='hospital_profile')
    hospitalId = models.CharField(max_length=20)
    
class VendorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='vendor_profile')
    gstin = models.CharField(max_length=20)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
