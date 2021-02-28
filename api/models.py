from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models


class Profile(models.Model):
    email = models.CharField(max_length=600, blank=False, null=False)
    password = models.CharField(max_length=600, blank=False, null=False)
    zip_code = models.CharField(max_length=500, null=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: "
                                         "'+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    def __str__(self):
        return self.email


class Code(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False)
    code = models.CharField(max_length=500, null=False)
    date_used = models.DateField(auto_now=True)
    status = models.CharField(max_length=100)
    balance_before = models.FloatField()
    balance_after = models.FloatField()
