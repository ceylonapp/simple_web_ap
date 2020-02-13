from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import deletion


class WebUser(models.Model):
    user = models.OneToOneField(User, on_delete=deletion.CASCADE, primary_key=True)

    def __str__(self):
        return f"{self.user.username}"

    @property
    def auth_user(self):
        return self.user
