from rest_framework import serializers

from library_api.models.transaction import Transaction


class TransactionSerializer(serializers.ModelSerializer):
   class Meta:
      model = Transaction
      fields = ["id", "issued_datetime", "book_id", "member_id", "returned_datetime", "overdue_fee", "fee_paid"]


class BookReturnSerializer(serializers.Serializer):
   member_id = serializers.IntegerField()
   book_id = serializers.IntegerField()
   fee_paid = serializers.IntegerField()

   def validate_fee_paid(self, value):
      if isinstance(value, str) or value < 0:
         raise serializers.ValidationError("Fee must be a positive integer")
      return value
