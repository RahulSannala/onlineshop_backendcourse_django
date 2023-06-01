from onlineshop_app.models import Order
from onlineshop_app.api.serializers import OrderSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from django.core.mail import send_mail
from django.conf import settings


def custom_mail(name, customer_email):
    subject = "New order is placed"
    message = f"Dear {name}, your order is placed successfully. Thanks for your order."
    recipient_list = [customer_email]

    send_mail(subject, message, settings.EMAIL_HOST_USER,
              recipient_list, fail_silently=False)


class OrderView(APIView):

    def get(self, request):
        try:
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
            return Response({
                'data': serializer.data,
                'message': "Orders data fetched successfully."
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                'data': {},
                'message': "Something went wrong while fetching the data."
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def post(self, request):

        try:
            data = request.data
            serializer = OrderSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'You sent a bad request'
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                customer_name = data.get('customer_name')
                customer_email = data.get('customer_email')
                custom_mail(name=customer_name, customer_email=customer_email)
                serializer.save()
                return Response({
                    'data': serializer.data,
                    'message': "Order was placed successfully"
                }, status=status.HTTP_201_CREATED)
        except:
            return Response({
                'data': {},
                'message': "Something went wrong in creation of order"
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def patch(self, request):
        try:
            data = request.data
            order = Order.objects.filter(id=data.get('id'))

            if not order.exists():
                return Response({
                    'data': {},
                    'message': "Order is not found with this ID."
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = OrderSerializer(
                instance=order[0], data=data, partial=True)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'You sent a bad request'
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({
                'data': serializer.data,
                'message': "Order was updated successfully"
            }, status=status.HTTP_200_OK)

        except:
            return Response({
                'data': {},
                'message': "Something went wrong in updating the order"
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def delete(self, request):

        try:
            data = request.data
            order = Order.objects.filter(id=data.get('id'))
            if not order.exists():
                return Response({
                    'data': {},
                    'message': "Order is not found with this ID."
                }, status=status.HTTP_404_NOT_FOUND)

            order[0].delete()

            return Response({
                'data': {},
                'message': "Order was deleted successfully"
            }, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({
                'data': {},
                'message': "Something went wrong in deleting the order"
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
