from rest_framework import viewsets, permissions
from customer.serializers import CustomerSerializer
from customer.models import Customer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]
