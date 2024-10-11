from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

from library_api.models.member import Member
from library_api.serializers.member import MemberSerializer


class MembersView(ListCreateAPIView):
   serializer_class = MemberSerializer
   queryset = Member.objects.all()


class MemberDetailView(RetrieveUpdateDestroyAPIView):
   serializer_class = MemberSerializer
   queryset = Member.objects.all()

