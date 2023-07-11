from .serializers import RegisterSerializer
from .models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import GenericAPIView

# Create your views here.
class RegisterView(GenericAPIView):
	serializer_class = RegisterSerializer

	def post(self, request):
		serializer = RegisterSerializer(data=request.data)
		if(serializer.is_valid()):
			serializer.save()
			return Response({
				"Message": "User Created Successfully",
				"User": serializer.data},
					status=status.HTTP_201_CREATED
			)
		return Response({
			"Errors": serializer.errors},
				status=status.HTTP_400_BAD_REQUEST
		)


class LoginView(APIView):
	def post(self, request):
		email = request.data['email']
		password = request.data['password']

		user = User.objects.filter(email=email).first()
		if user is None:
					raise AuthenticationFailed('User not found!')

		if not user.check_password(password):
			raise AuthenticationFailed('Incorrect Password')

		##### JWT Token ######
		try:
			refresh = RefreshToken.for_user(user)
		except ValidationError:
			raise serializers.ValidationError("Invalid Token.")

		return Response({
			'refresh': str(refresh),
			'access': str(refresh.access_token),
		})


class UserView(GenericAPIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticated]
	serializer_class = RegisterSerializer

	def get(self, request):
		user_obj = RegisterSerializer(request.user)
		return Response({'status': 200, 
			'payload': user_obj.data
		})
