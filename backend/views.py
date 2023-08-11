from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Customer

class CustomerListAPIView(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        customer_data = []
        for customer in customers:
            customer_data.append({
                'id': customer.id,
                'name': customer.name,
                'gender': customer.gender,
                'phone': customer.phone,
                'notes': customer.notes,
                'type': customer.type
            })
        return Response(customer_data, status=status.HTTP_200_OK)
    @transaction.atomic
    def post(self, request):
        try:
            data = request.data
            customer = Customer(name=data.get('name'), gender=data.get('gender'),phone=data.get('phone'),notes=data.get('notes'),type=data.get('type'))
            customer.save()
            return Response({'message': 'Customer created', 'customer': customer.get_json()}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)