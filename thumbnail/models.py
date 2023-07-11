from django.db import models
from product.models import Product


# Create your models here.
class Thumbnail(models.Model):
	product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
	product_image = models.ImageField(upload_to="mart/images", default='')

	def __int__(self):
		return self.id
