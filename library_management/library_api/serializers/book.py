from rest_framework.serializers import ModelSerializer, DateField

from library_api.models.book import Book


class BookSerializer(ModelSerializer):
   published_date = DateField(input_formats=['%m/%d/%Y', '%d-%m-%Y'])

   class Meta:
      model = Book
      fields = ["id", "title", "authors", "published_date", "publisher", "rental_fee", "available_count", "created_at"]
      read_only_fields = ["id", "created_at"]
