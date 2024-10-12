from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
import requests

from library_api.models.book import Book
from library_api.serializers.book import BookSerializer


class BooksView(APIView):
    def add_books(self, payload):
      books = []
      errors = []
      for book in payload:
          serializer = BookSerializer(data=book)
          if serializer.is_valid(): books.append(serializer.validated_data)
          else: errors.append(serializer.errors)

      if errors:
        return Response({"message": errors}, status=status.HTTP_400_BAD_REQUEST)

      books_to_create = [Book(**book) for book in books]
      created_books = Book.objects.bulk_create(books_to_create)
      books_serializer = BookSerializer(created_books, many=True)
      return Response(books_serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
      if request.path.endswith('import/'): return self.import_books()

      query = request.query_params.get('q', '').strip()
      books = Book.objects.filter(Q(title__icontains=query) | Q(authors__icontains=query))
      serializer = BookSerializer(books, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
      return self.add_books(request.data)

    def import_books(self):
      url_to_import_books = "https://frappe.io/api/method/frappe-library"
      try:
        response = requests.get(url_to_import_books)
        if response.status_code != 200:
          return Response({"message": "Failed to fetch data from Frappe"},
              status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response_json = response.json()
        books = []
        for book in response_json['message']:
          books.append({'title': book['title'], 'authors': book['authors'], 'publisher': book['publisher'], 'published_date': book['publication_date'], 'available_count': 10, 'rental_fee': 250 })

        return self.add_books(books)
      except Exception as e:
          return Response({"message": str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BookDetailView(APIView):
  def get(self, request, pk):
    book = get_object_or_404(Book, pk=pk)
    serializer = BookSerializer(book)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def patch(self, request, pk):
    book = get_object_or_404(Book, pk=pk)

    serializer = BookSerializer(book, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk):
      book = get_object_or_404(Book, pk=pk)

      book.delete()
      return Response({"message": "Book deleted successfully."}, status=status.HTTP_204_NO_CONTENT)