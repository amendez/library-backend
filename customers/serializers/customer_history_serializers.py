from rest_framework import serializers

from books.serializers import ConciseBookSerializer
from customers.models import CustomerHistory
from customers.serializers import ConciseCustomerSerializer


class CustomerHistorySerializer(serializers.ModelSerializer):
    book = ConciseBookSerializer()
    customer = ConciseCustomerSerializer()

    class Meta:
        model = CustomerHistory
        fields = [
            "id",
            "action",
            "book",
            "customer",
            "date_created",
        ]
