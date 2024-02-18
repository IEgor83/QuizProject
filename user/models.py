from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **extra_fields):
        if username is None:
            raise TypeError('Необходимо ввести имя пользователя')

        if email is None:
            raise TypeError('Необходимо ввести email')

        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(db_index=True, unique=True)
    username = models.CharField(db_index=True, max_length=255)
    date_joined = models.DateTimeField(default=timezone.now)
    password_updated_at = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()

    def set_password(self, raw_password):
        super().set_password(raw_password=raw_password)
        if self.pk is not None:
            self.password_updated_at = timezone.now()
            self.save(update_fields=["password_updated_at"])

    def __str__(self):
        return self.email
