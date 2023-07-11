from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Contact
from .serializers import ContactSerializer
from rest_framework.generics import GenericAPIView


# Create your views here.
class ContactAPI(GenericAPIView):
    serializer_class = ContactSerializer

    def get(self, request, pk=None, format=None):
        '''
        List all the Contact items for given requested user
        '''
        id = pk
        if id is not None:
            contact = Contact.objects.get(id=id)
            serializer = ContactSerializer(contact)
            return Response(serializer.data)

        contact = Contact.objects.all()
        serializer = ContactSerializer(contact, many=True)
        return Response(serializer.data)


    def post(self, request, format=None):
        '''
        Create the contact with the given contact data
        '''
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "Message": "Contact Created Successfully"},
                    status=status.HTTP_201_CREATED
            )
        return Response({
            "Errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
        )


    def put(self, request, pk, format=None):
        '''
        Updates the contact item with given category_id if exists
        '''
        id = pk
        contact = Contact.objects.get(pk=id)
        serializer = ContactSerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "Message": "Contact Updated Successfully"
            })
        return Response({
            "Errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
        )


    def patch(self, request, pk, format=None):
        id = pk
        contact = Contact.objects.get(pk=id)
        serializer = ContactSerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "Message": "Partial Contact Updated Successfully"
            })
        return Response({
            "Errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
        )


    def delete(self, request, pk, format=None):
        '''
        Deletes the contact item with given category_id if exists
        '''
        id = pk
        contact = Contact.objects.get(pk=id)
        contact.delete()
        return Response({
            "Message": "Contact Deleted"
        })


