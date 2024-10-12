from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.utils import timezone

from library_api.serializers.transaction import TransactionSerializer, BookReturnSerializer
from library_api.models.transaction import Transaction
from library_api.models.book import Book
from library_api.models.member import Member


class TransactionsView(ListCreateAPIView):
   serializer_class = TransactionSerializer
   queryset = Transaction.objects.all()

   def create(self, request):
      payload = request.data
      book_id = payload.get("book_id")
      member_id = payload.get("member_id")

      try:
         with transaction.atomic():
            # Validating book availability
            book = Book.objects.get(id=book_id)
            if book.available_count == 0:
               return Response({"message": "Book is not available"}, status=status.HTTP_400_BAD_REQUEST)

            # Validating member debt
            member = Member.objects.get(id=member_id)
            if member.debt >= 500:
               return Response({"message": "Member debt exceeds 500"}, status=status.HTTP_400_BAD_REQUEST)

            try:
               book_transaction = Transaction.objects.get(book_id=book_id, member_id=member_id, returned_datetime=None)
               return Response({"message": "Member already took the book"}, status=status.HTTP_400_BAD_REQUEST)
            except Transaction.DoesNotExist:
               pass

            serializer = TransactionSerializer(data=payload)
            if serializer.is_valid():
               serializer.save()
               book.available_count -= 1
               book.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      except Book.DoesNotExist:
         return Response({"message": "Book not found"}, status=status.HTTP_400_BAD_REQUEST)
      except Member.DoesNotExist:
         return Response({"message": "Member not found"}, status=status.HTTP_400_BAD_REQUEST)
      except Exception as e:
         return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class TransactionDetailView(RetrieveDestroyAPIView):
   serializer_class = TransactionSerializer
   queryset = Transaction.objects.all()


class TransactionReturnView(APIView):
   def post(self, request):
      payload = request.data
      book_id = payload.get("book_id")
      member_id = payload.get("member_id")
      fee_paid = payload.get("fee_paid", 0)

      try:
         serializer = BookReturnSerializer(data=payload)
         if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

         with transaction.atomic():
            book_transaction = Transaction.objects.get(book_id=book_id, member_id=member_id, returned_datetime=None)
            book = Book.objects.get(id=book_id)
            member = Member.objects.get(id=member_id)

            now = timezone.now()
            rented_days = (now - book_transaction.issued_datetime).days

            overdue_fee = 0
            if rented_days > 30: overdue_fee = 250

            total_fee = book.rental_fee + overdue_fee - fee_paid

            member.debt += total_fee
            book.available_count += 1

            book_transaction.overdue_fee = overdue_fee
            book_transaction.fee_paid = fee_paid
            book_transaction.returned_datetime = now

            book_transaction.save()
            member.save()
            book.save()
            return Response({"message": "Book returned successfully"}, status=status.HTTP_200_OK)

      except Book.DoesNotExist:
         return Response({"message": "Book not found"}, status=status.HTTP_400_BAD_REQUEST)
      except Transaction.DoesNotExist:
         return Response({"message": "Transaction not found"}, status=status.HTTP_400_BAD_REQUEST)
      except Exception as e:
         return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

