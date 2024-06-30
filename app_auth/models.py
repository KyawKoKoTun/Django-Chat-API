from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
import datetime
from django.utils import timezone

from .managers import CustomUserManager

import random


class User(AbstractUser):
    user_id = models.CharField(max_length=20, unique=True)
    last_login_ip = models.CharField(
        max_length=45,
        blank=True,
        null=True,
        help_text=_("IP address of the last login"),
    )
    last_active = models.DateTimeField(auto_now_add=True)

    email = models.EmailField(_("email address"), unique=True)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    username = models.CharField(max_length=1024, null=False, unique=False)
    photo = models.ImageField(
        upload_to="profile_photo/", default="profile_photo/default.png"
    )
    date_of_birth = models.DateField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.user_id:
            while True:
                new_id = "USER_" + "".join(
                    [str(random.randint(0, 9)) for _ in range(8)]
                )
                if not User.objects.filter(user_id=new_id).exists():
                    self.user_id = new_id
                    break
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} - {self.user_id})"


class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="otp")
    token = models.CharField(max_length=6, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_token(self):
        token = str(random.randint(100000, 999999))
        self.token = token
        self.save()
        return self.token

    def verify(self, token: str):
        if self.token and self.token == token:
            if timezone.now() - self.updated_at < datetime.timedelta(minutes=10):
                self.token = None
                self.save()
                return True
        return False
