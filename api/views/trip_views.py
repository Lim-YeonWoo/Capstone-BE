from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..serializers import *


class PersonalTripView(APIView):
    def get(self, request):
        pass


class GroupTripView(APIView):
    def get(self, request):
        pass