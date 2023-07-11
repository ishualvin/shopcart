from django.db import models
from category.models import Categry

# Create your models here.
class Subcategry(models.Model):
	name = models.CharField(max_length=300)
	category = models.ForeignKey(Categry, on_delete=models.CASCADE)

	def __str__(self):
		return self.name