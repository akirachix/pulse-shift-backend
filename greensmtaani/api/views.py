from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from users.models import Customer, MamaMboga
from django.db.models import Value as V, CharField, F
from .serializer import UserUnionSerializer, CustomerSerializer, MamaMbogaSerializer

class UserUnionList(APIView):
    def get(self, request):
        customers = Customer.objects.annotate(
            user_type=V('customer', output_field=CharField()),
            id=F('customer_id')
        ).values(
            'id', 'first_name', 'last_name', 'email', 'phone_number', 'password',
            'registration_date', 'is_active', 'user_type'
        )
        mamambogas = MamaMboga.objects.annotate(
            user_type=V('mama_mboga', output_field=CharField()),
            id=F('mama_mboga_id')
        ).values(
            'id', 'first_name', 'last_name', 'email', 'phone_number', 'password',
            'registration_date', 'is_active', 'user_type'
        )
        union = customers.union(mamambogas)
        serializer = UserUnionSerializer(union, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        user_type = data.get('user_type')
        if user_type == 'customer':
            serializer = CustomerSerializer(data=data)
        elif user_type == 'mama_mboga':
            serializer = MamaMbogaSerializer(data=data)
        else:
            return Response({'error': 'Unknown user_type'}, status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, pk):
        user_type = request.data.get('user_type')
        if user_type == 'customer':
            try:
                user = Customer.objects.get(pk=pk)
            except Customer.DoesNotExist:
                return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = CustomerSerializer(user, data=request.data, partial=True)
        elif user_type == 'mama_mboga':
            try:
                user = MamaMboga.objects.get(pk=pk)
            except MamaMboga.DoesNotExist:
                return Response({'error': 'MamaMboga not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = MamaMbogaSerializer(user, data=request.data, partial=True)
        else:
            return Response({'error': 'Invalid user_type'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user_type = request.data.get('user_type')
        if user_type == 'customer':
            try:
                user = Customer.objects.get(pk=pk)
            except Customer.DoesNotExist:
                return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
            user.delete()
        elif user_type == 'mama_mboga':
            try:
                user = MamaMboga.objects.get(pk=pk)
            except MamaMboga.DoesNotExist:
                return Response({'error': 'MamaMboga not found'}, status=status.HTTP_404_NOT_FOUND)
            user.delete()
        else:
            return Response({'error': 'Invalid user_type'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)