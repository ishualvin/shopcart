from django.db import models
from authentication.models import User
from product.models import Product

# Create your models here.
class Order(models.Model):

	STATUS = (
		("pending", "pending"),
		("completed", "completed"),
		("cancelled", "cancelled"),
	)
	order_buyer = models.ForeignKey(User, on_delete=models.CASCADE)
	order_product = models.ForeignKey(Product, on_delete=models.CASCADE)
	order_amount = models.CharField(max_length=25)
	order_id = models.CharField(max_length=100)
	payment_id = models.CharField(max_length=100)
	signature_id = models.CharField(max_length=100)
	isPaid = models.BooleanField(default=False)
	order_date = models.DateTimeField(auto_now=True)
	order_status = models.CharField(max_length=100, choices=STATUS, default='pending')

	def __str__(self):
		return self.order_status
