from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Subcategry
from .serializers import SubCategorySerializer
from rest_framework.generics import GenericAPIView


# Create your views here.
class SubCategoryAPI(GenericAPIView):
	serializer_class = SubCategorySerializer

	def get(self, request, pk=None, format=None):
		'''
		List all the subcategory items for given requested user
		'''
		id = pk
		if id is not None:
			subcategory = Subcategry.objects.get(id=id)
			serializer = SubCategorySerializer(subcategory)
			return Response(serializer.data)

		subcategory = Subcategry.objects.all()
		serializer = SubCategorySerializer(subcategory, many=True)
		return Response(serializer.data)


	def post(self, request, format=None):
		'''
		Create the subcategory with the given subcategory data
		'''
		serializer = SubCategorySerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({
				"Message": "SubCategory Created Successfully"},
				status=status.HTTP_201_CREATED
			)
		return Response({
			"Errors": serializer.errors},
			status=status.HTTP_400_BAD_REQUEST
        )


	def put(self, request, pk, format=None):
		'''
		Updates the subcategory item with given subcategory_id if exists
		'''
		id = pk
		subcategory = Subcategry.objects.get(pk=id)
		serializer = SubCategorySerializer(subcategory, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({
				"Message": "Subcategry Updated Successfully"
			})
		return Response({
			"Errors": serializer.errors},
			status=status.HTTP_400_BAD_REQUEST
		)


	def patch(self, request, pk, format=None):
		id = pk
		subcategory = Subcategry.objects.get(pk=id)
		serializer = SubCategorySerializer(subcategory, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({
				"Message": "Partial Subcategry Updated Successfully"
			})
		return Response({
			"Errors": serializer.errors},
			status=status.HTTP_400_BAD_REQUEST
		)


	def delete(self, request, pk, format=None):
		'''
		Deletes the subcategory item with given subcategory_id if exists
		'''
		id = pk
		subcategory = Subcategry.objects.get(pk=id)
		subcategory.delete()
		return Response({
			"Message": "Subcategry Deleted"
		})


