from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q

from library_api.models.book import Book
from library_api.serializers.book import BookSerializer


class BooksView(APIView):
    def post(self, request):
      serializer = BookSerializer(data=request.data)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
      query = request.query_params.get('q', '').strip()

      books = Book.objects.filter(Q(title__icontains=query) | Q(authors__icontains=query))
      serializer = BookSerializer(books, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)


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