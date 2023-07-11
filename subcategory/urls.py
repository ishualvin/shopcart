from django.urls import path
from .views import *

urlpatterns = [
	path('subcat/',SubCategoryAPI.as_view()),
	path('subcat/<int:pk>/',SubCategoryAPI.as_view()),
]