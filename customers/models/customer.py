from django.db import models


class Customer(models.Model):
    full_name = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.full_name
