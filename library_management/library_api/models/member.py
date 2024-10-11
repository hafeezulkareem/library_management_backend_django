from django.db import models


class Member(models.Model):
   name = models.CharField(max_length=250)
   email = models.EmailField(unique=True)
   phone_number = models.CharField(max_length=10, unique=True)
   address = models.TextField()
   debt = models.IntegerField(default=0, blank=True)
   created_at = models.DateTimeField(auto_now_add=True)

   def __str__(self):
      return self.name
