from django.db import models


class CustomerHistory(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, null=True, related_name="history")
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE, null=True, related_name="transactions")

    ACTION_CHOICES = (
        ('Check out', 'Check out'),
        ('Return', 'Return')
    )
    action = models.CharField(choices=ACTION_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.action}: {self.book} - {self.customer}"
