from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Categry
from .serializers import CategorySerializer
from rest_framework.generics import GenericAPIView


# Create your views here.
class CategoryAPI(GenericAPIView):
    serializer_class = CategorySerializer

    def get(self, request, pk=None, format=None):
        '''
        List all the category items for given requested user
        '''
        id = pk
        if id is not None:
            category = Categry.objects.get(id=id)
            serializer = CategorySerializer(category)
            return Response(serializer.data)

        category = Categry.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)


    def post(self, request, format=None):
        '''
        Create the category with the given category data
        '''
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "Message": "Category Created Successfully"},
                    status=status.HTTP_201_CREATED
            )
        return Response({
            "Errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
        )


    def put(self, request, pk, format=None):
        '''
        Updates the category item with given category_id if exists
        '''
        id = pk
        category = Categry.objects.get(pk=id)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "Message": "Category Updated Successfully"
            })
        return Response({
            "Errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
        )


    def patch(self, request, pk, format=None):
        id = pk
        category = Categry.objects.get(pk=id)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "Message": "Partial Category Updated Successfully"
            })
        return Response({
            "Errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
        )


    def delete(self, request, pk, format=None):
        '''
        Deletes the category item with given category_id if exists
        '''
        id = pk
        category = Categry.objects.get(pk=id)
        category.delete()
        return Response({
            "Message": "Category Deleted"
        })

