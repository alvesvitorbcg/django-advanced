from rest_framework import viewsets, permissions
from api import serializers
from customer.models import Customer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = serializers.CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]
