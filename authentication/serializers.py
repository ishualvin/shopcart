from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ['id', 'first_name', 'last_name', 'email', 'password', 'address', 'image',
					'city', 'country', 'zip_code', 'phone', 'is_seller', 'is_buyer']


	def create(self, validated_data):
		password = validated_data.pop('password', None) #removes and returns the last value from the List or the given index value
		instance = self.Meta.model(**validated_data)
		if password != None:
			instance.set_password(password)
		instance.save()
		return instance