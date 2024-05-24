from django.db import transaction
from rest_framework import serializers

from customers.models import Customer


class ConciseCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "full_name"]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "full_name",
            "date_created",
            "email",
        ]
        read_only_fields = ("date_created",)
