from django.shortcuts import render
from .models import Room
from .serializers import RoomSerializer
from rest_framework import generics

class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer