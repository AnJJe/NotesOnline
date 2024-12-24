# users/models.py
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Связь с моделью User
    is_admin = models.BooleanField(default=False)  # Флаг для определения роли админа

    def __str__(self):
        return self.user.username
