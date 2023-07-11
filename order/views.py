from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import Order
from product.models import Product
from .serializers import OrderSerializer
import json
import environ
import razorpay
from rest_framework.generics import GenericAPIView


env = environ.Env()

# you have to create .env file in same folder where you are using environ.Env()
# reading .env file which located in api folder
environ.Env.read_env()


# Create your views here.
class OrderAPI(GenericAPIView):
	serializer_class = OrderSerializer
	
	def get(self, request, pk=None, format=None):
		'''
		List all the order items for given requested user
		'''
		id = pk
		if id is not None:
			order = Order.objects.get(id=id)
			serializer = OrderSerializer(order)
			return Response(serializer.data)

		order = Order.objects.all()
		serializer = OrderSerializer(order, many=True)
		return Response(serializer.data)


	def post(self, request, format=None):
		'''
		Create the order with the given order data
		'''
		# request.data is coming from frontend
		user = request.user
		amount = request.data['order_amount']
		product_id = request.data['order_product']

		# setup razorpay client this is the client to whome user is paying money that's you
		client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))

		razorpay_order = client.order.create({"amount": int(amount) * 100,
									"currency": "INR",
									"payment_capture": "1"
									})

		order = Order.objects.create(order_product=Product.objects.get(id = product_id),
									order_amount=amount,
									order_buyer=user,
									order_id=razorpay_order['id']
									)

		serializer = OrderSerializer(order)

		"""order response will be 
		{
			"id": 3,
			"order_date": "09 October 2022 08:15 AM",
			"order_amount": "5",
			"order_payment_id": "order_KReEarBvxi2bgz",
			"isPaid": false,
			"order_status": "pending",
			"order_buyer": 2,
			"order_product": 1
		}"""

		data = {
			"Message": "Order Created Successfully",
			"payment": razorpay_order,
			"order": serializer.data
		}
		return Response(data)



	def put(self, request, pk, format=None):
		'''
		Updates the order item with given product_id if exists
		'''
		id = pk
		order = Order.objects.get(pk=id)
		serializer = OrderSerializer(order, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({
				"Message": "Order Updated Successfully"
			})
		return Response({
			"Errors": serializer.errors},
			status=status.HTTP_400_BAD_REQUEST
		)


	def patch(self, request, pk, format=None):
		id = pk
		order = Order.objects.get(pk=id)
		serializer = OrderSerializer(order, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({
				"Message": "Partial Order Updated Successfully"
			})
		return Response({
			"Errors": serializer.errors},
			status=status.HTTP_400_BAD_REQUEST
		)


	def delete(self, request, pk, format=None):
		'''
		Deletes the order item with given product_id if exists
		'''
		id = pk
		order = Order.objects.get(pk=id)
		order.delete()
		return Response({
			"Message": "Order Deleted"
		})



@api_view(['POST'])
def handle_payment_success(request):
    # request.data is coming from frontend
    res = json.loads(request.data["response"])
    print('>>>>', res)

    """res will be:
    {'razorpay_payment_id': 'pay_G3NivgSZLx7I9e', 
    'razorpay_order_id': 'order_G3NhfSWWh5UfjQ', 
    'razorpay_signature': '76b2accbefde6cd2392b5fbf098ebcbd4cb4ef8b78d62aa5cce553b2014993c0'}
    this will come from frontend which we will use to validate and confirm the payment
    """

    ord_id = ""
    raz_pay_id = ""
    raz_signature = ""

    # res.keys() will give us list of keys in res
    for key in res.keys():
        if key == 'razorpay_order_id':
            ord_id = res[key]
        elif key == 'razorpay_payment_id':
            raz_pay_id = res[key]
        elif key == 'razorpay_signature':
            raz_signature = res[key]

    # get order by payment_id which we've created earlier with isPaid=False
    order = Order.objects.get(order_payment_id=ord_id)

    # we will pass this whole data in razorpay client to verify the payment
    data = {
        'razorpay_order_id': ord_id,
        'razorpay_payment_id': raz_pay_id,
        'razorpay_signature': raz_signature
    }

    client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))

    # checking if the transaction is valid or not by passing above data dictionary in 
    # razorpay client if it is "valid" then check will return None
    check = client.utility.verify_payment_signature(data)

    if check is not None:
        print("Redirect to error url or error page")
        return Response({'error': 'Something went wrong'})

    # if payment is successful that means check is None then we will turn isPaid=True
    order.isPaid = True
    order.save()

    res_data = {
        'message': 'payment successfully received!'
    }

    return Response(res_data)



