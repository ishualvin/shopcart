from rest_framework import serializers
from .models import Categry


class CategorySerializer(serializers.ModelSerializer):

	class Meta:
		model = Categry
		fields = "__all__"