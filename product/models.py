from django.db import models
from authentication.models import User
from category.models import Categry
from subcategory.models import Subcategry


# Create your models here.
class Product(models.Model):
	seller = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	product_name = models.CharField(max_length=500)
	category = models.ForeignKey(Categry, on_delete=models.CASCADE)
	subcategory = models.ForeignKey(Subcategry, on_delete=models.CASCADE)
	price = models.IntegerField(default=0)
	description = models.TextField(max_length=900)
	published_date = models.DateField(auto_now_add=True)
	is_stock = models.BooleanField(default=True)

	def __str__(self):
		return self.product_name