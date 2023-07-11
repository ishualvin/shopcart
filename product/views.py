from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import ProductSerializer
from rest_framework.generics import GenericAPIView


# Create your views here.
class ProductAPI(GenericAPIView):
	permission_classes = (IsAuthenticated, )
	serializer_class = ProductSerializer
	
	def get(self, request, pk=None, format=None):
		'''
		List all the product items for given requested user
		'''
		id = pk
		if id is not None:
			product = Product.objects.get(id=id)
			serializer = ProductSerializer(product)
			return Response(serializer.data)

		product = Product.objects.all()
		serializer = ProductSerializer(product, many=True)
		return Response(serializer.data)


	def post(self, request, format=None):
		'''
		Create the product with the given product data
		'''
		serializer = ProductSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(seller=self.request.user)
			return Response({
				"Message": "Product Created Successfully"},
				status=status.HTTP_201_CREATED
			)
		return Response({
			"Errors": serializer.errors},
			status=status.HTTP_400_BAD_REQUEST
        )


	def put(self, request, pk, format=None):
		'''
		Updates the product item with given product_id if exists
		'''
		id = pk
		product = Product.objects.get(pk=id)
		serializer = ProductSerializer(product, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({
				"Message": "Product Updated Successfully"
			})
		return Response({
			"Errors": serializer.errors},
			status=status.HTTP_400_BAD_REQUEST
		)


	def patch(self, request, pk, format=None):
		id = pk
		product = Product.objects.get(pk=id)
		serializer = ProductSerializer(product, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({
				"Message": "Partial Product Updated Successfully"
			})
		return Response({
			"Errors": serializer.errors},
			status=status.HTTP_400_BAD_REQUEST
		)


	def delete(self, request, pk, format=None):
		'''
		Deletes the product item with given product_id if exists
		'''
		id = pk
		product = Product.objects.get(pk=id)
		product.delete()
		return Response({
			"Message": "Product Deleted"
		})


class ProductSearchAPI(ListAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	filter_backends = [SearchFilter]
	search_fields = ['^product_name', 'subcategory__name']




