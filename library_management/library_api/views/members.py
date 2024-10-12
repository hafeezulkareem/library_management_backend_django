from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from django.db.models import Q

from library_api.models.member import Member
from library_api.serializers.member import MemberSerializer


class MembersView(ListCreateAPIView):
   serializer_class = MemberSerializer

   def get_queryset(self):
      queryset = Member.objects.all()
      query = self.request.query_params.get('q', None)
      if query:
         queryset = queryset.filter(
               Q(name__icontains=query) |
               Q(email__icontains=query) |
               Q(phone_number__icontains=query)
         )
      return queryset


class MemberDetailView(RetrieveUpdateDestroyAPIView):
   serializer_class = MemberSerializer
   queryset = Member.objects.all()

