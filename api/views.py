# from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerialzer, UserSerializer
from django.contrib.auth.models import User


# Create your views here.

@api_view(['GET'])
def getRoutes(request):
    route = [
        'GET /api/',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    # safe means we can use more than just python dictionary
    # return JsonResponse(route, safe=False)
    return Response(route)


@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    return Response(RoomSerialzer(rooms, many=True).data)


@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    roomData = RoomSerialzer(room, many=False).data
    user = room.host.username
    topic = room.topic.name
    numberParticipants = roomData['participants']
    participantList = []
    for participantID in numberParticipants:
        participantList.append(UserSerializer(
            User.objects.get(id=participantID)).data["username"])
    context = {"participants": participantList, "Room Host": user,
               "Room Topic": topic, "Room info": roomData}

    return Response(context)
