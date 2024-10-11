from django.db import models
from django.core.validators import MinValueValidator

class Book(models.Model):
   title = models.CharField(max_length=500)
   authors = models.CharField(max_length=250)
   published_date = models.DateField()
   publisher = models.CharField(max_length=250)
   rental_fee = models.IntegerField(validators=[MinValueValidator(1)])
   available_count = models.IntegerField(validators=[MinValueValidator(0)])
   created_at = models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return self.title
