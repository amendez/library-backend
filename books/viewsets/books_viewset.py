from rest_framework import permissions, viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from books.models import Book
from books.serializers import ConciseBookSerializer, BookSerializer
from customers.models import Customer


class BooksViewSet(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin, viewsets.mixins.RetrieveModelMixin):
    queryset = Book.objects.all()
    serializer_class = ConciseBookSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["title", "format", "edition", "genres__name", "authors__full_name"]
    ordering_fields = ["title", "date_created", "pages", "rating", "rating_count", "review_count"]
    ordering = ["-date_created"]

    def get_serializer_class(self):
        if self.action == 'list':
            return ConciseBookSerializer
        return BookSerializer

    def get_queryset(self):
        return Book.objects.all().prefetch_related("authors", "genres")

    @action(detail=True, methods=["POST"], url_path="checkout")
    def checkout_book(self, request, pk=None):
        book = self.get_object()
        customer = Customer.objects.get(pk=request.data["customer"])
        try:
            book.checkout_book(customer)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        book.refresh_from_db()
        return Response(BookSerializer(book).data)

    @action(detail=True, methods=["POST"], url_path="return")
    def return_book(self, request, pk=None):
        book = self.get_object()
        customer = Customer.objects.get(pk=request.data["customer"])
        try:
            book.return_book(customer)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        book.refresh_from_db()
        return Response(BookSerializer(book).data)
