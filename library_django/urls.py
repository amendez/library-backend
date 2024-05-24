"""
URL configuration for library_django project.
"""
from django.contrib import admin
from django.urls import path
from rest_framework import routers

from books.viewsets import BooksViewSet
from customers.viewsets import CustomersViewSet

router = routers.DefaultRouter()
router.register(r'books', BooksViewSet)
router.register(r'customers', CustomersViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += router.urls
