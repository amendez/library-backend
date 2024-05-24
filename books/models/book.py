from django.db import models, transaction
from django.db.models import F

from customers.models import CustomerHistory


class Book(models.Model):
    FORMAT_CHOICES = (
        ('Audible Audio', 'Audible Audio'),
        ('Audio CD', 'Audio CD'),
        ('Audiobook', 'Audiobook'),
        ('Chapbook', 'Chapbook'),
        ('ebook', 'ebook'),
        ('Hardcover', 'Hardcover'),
        ('Kindle Edition', 'Kindle Edition'),
        ('Mass Market Paperback', 'Mass Market Paperback'),
        ('Nook', 'Nook'),
        ('Paperback', 'Paperback'),
        ('Trade Paperback', 'Trade Paperback'),
    )

    authors = models.ManyToManyField("Author", related_name="books")
    desc = models.TextField()
    edition = models.CharField(max_length=200, null=True, blank=True)
    format = models.CharField(choices=FORMAT_CHOICES, blank=True, null=True)
    genres = models.ManyToManyField("Genre", related_name="books")
    pages = models.IntegerField(default=0)
    rating = models.FloatField(default=0)
    rating_count = models.IntegerField(default=0)
    review_count = models.IntegerField(default=0)
    title = models.CharField(max_length=200)
    stock = models.IntegerField(default=1)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.format})"

    def checkout_book(self, customer):
        """
        Check out a book to a customer, decrementing the stock by 1 and storing the transaction in the history
        """
        with transaction.atomic():
            updated = Book.objects.filter(id=self.id).filter(stock__gt=0).update(stock=F('stock') - 1)
            if updated == 0:
                raise ValueError("No stock available")
            self.transactions.create(customer=customer, action="Check out")

    def return_book(self, customer):
        """
        Return a book from a customer, incrementing the stock by 1 and storing the transaction in the history
        """
        with transaction.atomic():
            try:
                history = customer.history.filter(book=self).latest('date_created')
            except CustomerHistory.DoesNotExist:
                history = None

            if not history or history.action != "Check out":
                raise ValueError("Book already returned or never checked out")
            Book.objects.filter(id=self.id).update(stock=F('stock') + 1)
            self.transactions.create(customer=customer, action="Return")
