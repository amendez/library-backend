from django.test import TestCase

from books.models import Book
from customers.models import Customer


class TestCheckOutAndReturnBooks(TestCase):

    @classmethod
    def setUp(self):
        self.book_1 = Book.objects.create(title="Book 1")
        self.book_2 = Book.objects.create(title="Book 2", stock=0)
        self.customer_1 = Customer.objects.create(full_name="Customer 1")
        self.customer_2 = Customer.objects.create(full_name="Customer 1")

    def test_checkout_book_should_decrease_book_stock(self):
        self.assertEqual(self.book_1.stock, 1)
        self.book_1.checkout_book(self.customer_1)
        self.book_1.refresh_from_db()
        self.assertEqual(self.book_1.stock, 0)

    def test_return_book_should_increase_book_stock(self):
        self.assertEqual(self.book_1.stock, 1)
        self.book_1.checkout_book(self.customer_1)
        self.book_1.refresh_from_db()
        self.assertEqual(self.book_1.stock, 0)
        self.book_1.return_book(self.customer_1)
        self.book_1.refresh_from_db()
        self.assertEqual(self.book_1.stock, 1)

    def test_cant_checkout_book_with_no_stock(self):
        self.assertEqual(self.book_2.stock, 0)
        with self.assertRaises(ValueError):
            self.book_2.checkout_book(self.customer_1)
        self.book_2.refresh_from_db()
        self.assertEqual(self.book_2.stock, 0)

    def test_customer_cant_return_book_not_checked_our(self):
        self.assertEqual(self.book_1.stock, 1)
        with self.assertRaises(ValueError):
            self.book_1.return_book(self.customer_1)
        self.book_1.refresh_from_db()
        self.assertEqual(self.book_1.stock, 1)

    def test_customer_cant_return_book_twice(self):
        self.assertEqual(self.book_1.stock, 1)
        self.book_1.checkout_book(self.customer_1)
        self.book_1.refresh_from_db()
        self.assertEqual(self.book_1.stock, 0)
        self.book_1.return_book(self.customer_1)
        self.book_1.refresh_from_db()
        self.assertEqual(self.book_1.stock, 1)
        with self.assertRaises(ValueError):
            self.book_1.return_book(self.customer_1)
        self.book_1.refresh_from_db()
        self.assertEqual(self.book_1.stock, 1)

    def test_customer_cant_return_book_from_another_customer(self):
        self.assertEqual(self.book_1.stock, 1)
        self.book_1.checkout_book(self.customer_1)
        self.book_1.refresh_from_db()
        self.assertEqual(self.book_1.stock, 0)
        with self.assertRaises(ValueError):
            self.book_1.return_book(self.customer_2)
        self.book_1.refresh_from_db()
        self.assertEqual(self.book_1.stock, 0)

    def test_checkout_book_should_store_transaction_in_history(self):
        self.assertEqual(self.book_1.stock, 1)
        self.assertEqual(self.customer_1.history.count(), 0)
        self.book_1.checkout_book(self.customer_1)
        self.book_1.refresh_from_db()
        self.assertEqual(self.book_1.stock, 0)
        self.assertEqual(self.customer_1.history.count(), 1)
        self.assertEqual(self.customer_1.history.first().action, "Check out")

    def test_return_book_should_store_transaction_in_history(self):
        self.assertEqual(self.book_1.stock, 1)
        self.assertEqual(self.customer_1.history.count(), 0)
        self.book_1.checkout_book(self.customer_1)
        self.book_1.refresh_from_db()
        self.assertEqual(self.book_1.stock, 0)
        self.assertEqual(self.customer_1.history.count(), 1)
        self.assertEqual(self.customer_1.history.first().action, "Check out")
        self.book_1.return_book(self.customer_1)
        self.book_1.refresh_from_db()
        self.assertEqual(self.book_1.stock, 1)
        self.assertEqual(self.customer_1.history.count(), 2)
        self.assertEqual(self.customer_1.history.first().action, "Check out")
        self.assertEqual(self.customer_1.history.last().action, "Return")
