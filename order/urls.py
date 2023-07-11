from django.urls import path
from .views import *

urlpatterns = [
	path('ord/',OrderAPI.as_view()),
	path('ord/<int:pk>/',OrderAPI.as_view()),
	path('ord/success/', handle_payment_success)

]