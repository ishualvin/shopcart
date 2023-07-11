from django.urls import path
from .views import *

urlpatterns = [
	path('cont/',ContactAPI.as_view()),
	path('cont/<int:pk>/',ContactAPI.as_view()),

]