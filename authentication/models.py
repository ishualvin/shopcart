from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
	email = models.CharField(max_length=255, unique=True, default="")
	image = models.ImageField(upload_to="mart/images", default='')
	address = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	country = models.CharField(max_length=50)
	zip_code = models.CharField(max_length=50)
	phone = models.CharField(max_length=50, default="")
	is_seller = models.BooleanField(default=False)
	is_buyer = models.BooleanField(default=False)


	def __str__(self):
		return self.email
