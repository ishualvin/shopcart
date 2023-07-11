from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Thumbnail
from .serializers import ThumbnailSerializer
from rest_framework.generics import GenericAPIView


# Create your views here.
class ProductImageAPI(GenericAPIView):
	serializer_class = ThumbnailSerializer
	
	def get(self, request, pk=None, format=None):
		'''
		List all the thumbnail items for given requested user
		'''
		id = pk
		if id is not None:
			thumbnail = Thumbnail.objects.get(id=id)
			serializer = ThumbnailSerializer(thumbnail)
			return Response(serializer.data)

		thumbnail = Thumbnail.objects.all()
		serializer = ThumbnailSerializer(thumbnail, many=True)
		return Response(serializer.data)


	def post(self, request, format=None):
		'''
		Create the thumbnail with the given thumbnail data
		'''
		serializer = ThumbnailSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({
				"Message": "Thumbnail Created Successfully"},
				status=status.HTTP_201_CREATED
			)
		return Response({
			"Errors": serializer.errors},
			status=status.HTTP_400_BAD_REQUEST
        )


	def put(self, request, pk, format=None):
		'''
		Updates the thumbnail item with given product_id if exists
		'''
		id = pk
		thumbnail = Thumbnail.objects.get(pk=id)
		serializer = ThumbnailSerializer(thumbnail, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({
				"Message": "Thumbnail Updated Successfully"
			})
		return Response({
			"Errors": serializer.errors},
			status=status.HTTP_400_BAD_REQUEST
		)


	def patch(self, request, pk, format=None):
		id = pk
		thumbnail = Thumbnail.objects.get(pk=id)
		serializer = ThumbnailSerializer(thumbnail, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({
				"Message": "Partial Thumbnail Updated Successfully"
			})
		return Response({
			"Errors": serializer.errors},
			status=status.HTTP_400_BAD_REQUEST
		)


	def delete(self, request, pk, format=None):
		'''
		Deletes the thumbnail item with given product_id if exists
		'''
		id = pk
		thumbnail = Thumbnail.objects.get(pk=id)
		thumbnail.delete()
		return Response({
			"Message": "Thumbnail Deleted"
		})