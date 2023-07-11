from rest_framework import serializers
from .models import Subcategry


class SubCategorySerializer(serializers.ModelSerializer):

	class Meta:
		model = Subcategry
		fields = "__all__"