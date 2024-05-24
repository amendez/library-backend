from rest_framework import permissions, viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from customers.models import Customer
from customers.serializers import ConciseCustomerSerializer, CustomerSerializer, CustomerHistorySerializer


class CustomersViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'list':
            return ConciseCustomerSerializer
        return CustomerSerializer

    @action(detail=True, methods=["GET"], url_path="history")
    def history(self, request, pk=None):
        customer = self.get_object()
        history = customer.history.all()
        serializer = CustomerHistorySerializer(history, many=True)
        return Response(serializer.data)