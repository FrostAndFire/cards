from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractBaseUser#, BaseUserManager


# custom User model

#class CUserManager(BaseUserManager):
#    use_in_migrations = True
#    def create_superuser(self, username, password, is_staff, is_superuser):
#        user = self.model(                       
#                          is_staff = True,
#                          is_superuser = True
#                          )
#        user.set_password(password)
#        user.save(using=self._db)
#        return user

class CUserModel(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True, null=False, blank=False)
    email = models.EmailField(max_length=254, unique=True, null=False, blank=False)
    is_superuser = models.BooleanField()
    is_staff = models.BooleanField()
    is_active = models.BooleanField(default=True)
    #date_joined = models.DateTimeField()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    objects = UserManager()

# app models

class Card(models.Model):
    name = models.CharField(max_length=200)
    content = models.CharField(max_length=1000)
    avg_rating = models.IntegerField(default=0)

class Rating(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    user = models.ForeignKey(CUserModel, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True, blank=True)
