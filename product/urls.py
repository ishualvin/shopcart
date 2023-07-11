from django.urls import path
from .views import *

urlpatterns = [
	path('prod/',ProductAPI.as_view()),
	path('prod/<int:pk>/',ProductAPI.as_view()),
	path('prodsearch/',ProductSearchAPI.as_view()),

]