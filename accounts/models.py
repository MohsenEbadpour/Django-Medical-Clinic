from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager
from django.urls import reverse
from django.conf import settings 

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Email Address', unique=True)
    date_joined = models.DateTimeField('Date Joined', auto_now_add=True)
    is_active = models.BooleanField('Active', default=True)
    objects = UserManager()
    is_staff = models.BooleanField('Staff Status',default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_name(self):
        full_name = '%s' % (self.name)
        return full_name.strip()

    def get_url(self):
        return reverse("accounts:home")



class Doctor(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	id_number = models.IntegerField(unique=True)
	name = models.CharField(max_length=50)
	phone = models.IntegerField()
	cash = models.PositiveIntegerField(default=0)

	def __str__(self):
		return str(self.name)

	def get_url(self):
		return reverse("accounts:home")


class Sick(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	id_number = models.IntegerField(unique=True)
	name = models.CharField(max_length=50)
	phone = models.IntegerField()
	cash = models.PositiveIntegerField(default=0)

	def __str__(self):
		return str(self.name)
		
	def get_url(self):
		return reverse("accounts:home")




class Staff(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	id_number = models.IntegerField(default=0)
	name = models.CharField(max_length=50)
	phone = models.IntegerField(default=0)

	def __str__(self):
		return str(self.name)

	def get_url(self):
		return reverse("accounts:home")






