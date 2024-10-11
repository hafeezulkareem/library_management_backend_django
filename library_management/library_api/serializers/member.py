from rest_framework.serializers import ModelSerializer

from library_api.models.member import Member


class MemberSerializer(ModelSerializer):
   class Meta:
      model = Member
      fields = ["id", "name", "email", "phone_number", "address", "debt", "created_at"]
      read_only_fields = ["id", "created_at"]
