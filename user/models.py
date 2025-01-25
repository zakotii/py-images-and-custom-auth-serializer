from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager


class User(AbstractUser):
    pass


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, username=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        
        # Исправление: добавляем username, если он отсутствует
        if not username:
            raise ValueError("The Username field must be set")
        
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
