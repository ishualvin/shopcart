from django.urls import path
from .views import *

urlpatterns = [
	path('image/',ProductImageAPI.as_view()),
	path('image/<int:pk>/',ProductImageAPI.as_view()),
]