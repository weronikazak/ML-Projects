from django.shortcuts import render
from .models import Room
from .serializers import RoomSerializer, CreateRoomSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.response import JsonResponse

class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kward = "code"

    def get(self, request, format=None):
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            room = Room.objects.filter(code=code)
            if len(room) > 0:
                data = RoomSerializer(room[0]).data
                data["is_host"] = self.request.session.session_key == room[0].host
                return Response(data, status=status.HTTP_200_OK)
            return Response({"Room Not Found":"Invalid Room Code"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"Bad Request":"Code parameter not found in request"}, status=status.HTTP_400_BAD_REQUEST)


class JoinRoom(APIView):
    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        
        code = request.session.create()
        if code != None:
            room_result = Room.objects.filter(code=code)
            if len(room_result) > 0:
                room = room_result[0]
                self.request.session["room_code"] = code
                return Response({"message": "Room Joined"}, status=status.HTTP_200_OK)
            return Response({"Bad Request": "Invalid room code"}, status=status.HTTP_400_REQUEST)
        
        return Response({"Bad Request": "Invalid post data, did nt find a code key"}, status=status.HTTP_400_REQUEST)


class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get("guest_can_pause")
            votes_to_skip = serializer.data.get("votes_to_skip")
            host = self.request.session.session_key
            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=["guest_can_pause", "votes_to_skip"])
                self.request.session["room_code"] = room.code
                return Response(RoomSerializer(room).data, status=status)
            else:
                room = Room(host=host, guest_can_pause=guest_can_pause,
                            votes_to_skip = votes_to_skip)
                room.save()
                self.request.session["room_code"] = room.code    
                return Response(RoomSerializer(room).data, status=status)

class UserInRoom(APIView):
    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
           self.request.session.create()
        data = {
            "code": self.request.session.get("room_code")
        }

        return JsonResponse(data, status=status.HTTP_200_OK) 