from django.urls import path
from .views import *

urlpatterns = [
	path('cat/',CategoryAPI.as_view()),
	path('cat/<int:pk>/',CategoryAPI.as_view()),

]