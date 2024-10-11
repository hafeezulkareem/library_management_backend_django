from django.db import models

from .book import Book
from .member import Member


class Transaction(models.Model):
   issued_datetime = models.DateTimeField(auto_now_add=True)
   book_id = models.ForeignKey(to=Book, on_delete=models.SET_NULL, null=True)
   member_id = models.ForeignKey(to=Member, on_delete=models.SET_NULL, null=True)
   returned_datetime = models.DateTimeField(blank=True, null=True)
   overdue_fee = models.IntegerField(default=0, blank=True)
   fee_paid = models.IntegerField(default=0, blank=True)
