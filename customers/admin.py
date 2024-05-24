from django.contrib import admin

from customers.models import Customer,CustomerHistory

admin.site.register(Customer)
admin.site.register(CustomerHistory)
