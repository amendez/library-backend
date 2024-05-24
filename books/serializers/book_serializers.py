from django.db import transaction
from rest_framework import serializers

from books.models import Book


class ConciseBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "format", "edition"]


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.StringRelatedField(many=True)
    genres = serializers.StringRelatedField(many=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "authors",
            "date_created",
            "desc",
            "edition",
            "format",
            "genres",
            "pages",
            "rating",
            "rating_count",
            "review_count",
            "title",
            "stock"
        ]
        read_only_fields = ("date_created", "stock", "rating", "rating_count", "review_count")
