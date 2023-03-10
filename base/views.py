from django.shortcuts import render, redirect
from .models import Room, Topic, Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
# from django.http import HttpResponse

# template inheritence
# use {% include 'nav.html' %} over all htmls to inherit its properties
# now the inheritence part, use main as the structure of the html file with blocks extending the main.html when they are called.


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:  # to check if the user even exists
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User doesn\'t exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password doesn\'t exist')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    # print("Logout Testing")
    # this will basically delete the session id and hence the cookie won't work and will be deleted?
    logout(request)
    return redirect('home')


def registerUser(request):
    page = 'register'

    if request.method == 'POST':
        # username=request.POST.get('username')
        # password=request.POST.get('password')
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # we are saving the form but freezing it in time here
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            # login(request,user) #this is for immediate login.. i prefer to send them to login page first
            return redirect('login')
        else:
            messages.error(request, "please enter valid username and password")

    form = UserCreationForm()
    context = {'page': page, "form": form}
    return render(request, 'base/login_register.html', context)


def home(request):  # request object is http object which tells us the kind of request method is sent and the kind of data that is being sent as a request
    # return HttpResponse("Home page")
    q = request.GET.get('q')
    # print(request)
    print(request.user)
    # return request

    if q != None:

        rooms = Room.objects.filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(host__username__icontains=q)

        )
        room_messages = Message.objects.filter(Q(room__name__icontains=q) | Q(
            room__topic__name__icontains=q) | Q(room__host__username__icontains=q)).order_by('-created')

    else:

        rooms = Room.objects.filter()
        room_messages = Message.objects.filter().order_by('-created')
    # slower version is len(rooms) since rooms is basically a list of dictionaries after all
    room_count = rooms.count()
    topic = Topic.objects.all()

    context = {"rooms": rooms, "topic": topic,
               "room_count": room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)


def room(request, pk):
    # return HttpResponse("ROOM")

    # i don't understand why is integer matching with string.. is it converting internally?
    room = Room.objects.get(id=pk)
    texts = room.message_set.all().order_by('created')
    participants = room.participants.all()
    if request.method == 'POST':
        text = Message.objects.create(
            user=request.user, room=room, body=request.POST.get('text'))
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    # for i in rooms:
    #     if i.id==int(pk):
    #         room=i
    #         context={"room":room}
    # The above also woks
    context = {"room": room, "texts": texts, 'participants': participants}

    return render(request, 'base/room.html', context)


def userProfile(request, pk):
    person = User.objects.get(id=pk)
    room_messages = Message.objects.filter(
        Q(user__username=person.username)).order_by('-created')
    context = {'user': person, 'room_messages': room_messages}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    # print("here is the crazy part:",request.headers)
    form = RoomForm()

    if (request.method == 'POST'):

        # as far as i understood, the form will extract the values from the request sent by the form.html upon last createRoom call
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def createTopic(request):

    if request.method == 'POST':
        new_topic = request.POST.get('new_topic')
        p = Topic(name=new_topic)
        p.save()
        return redirect('home')
    context = {}
    return render(request, 'base/topic_create.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):

    room = Room.objects.get(id=pk)
    # form is filled up with the id=pk data in room table.
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not allowed here!!")

    if (request.method == 'POST'):

        # as far as i understood, the form will extract the values from the request sent by the form.html upon last createRoom call
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def deleteRoom(request, pk):
    # print("delete room views is entered")
    room = Room.objects.get(id=pk)
    context = {"obj": room}
    if request.user != room.host:
        return HttpResponse("You are not allowed here!!")
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    # print("control flow just before rendering")
    return render(request, 'base/delete.html', context)


def deleteMessage(request, pk):
    # print("delete room views is entered")
    text = Message.objects.get(id=pk)

    context = {"obj": text}
    if request.user != text.user:
        return HttpResponse("You are not allowed here!!")
    if request.method == 'POST':
        text.delete()
        return redirect('room', pk=text.room.id)
        # return render(request,'room/'+str(text.room.id),context)
    # print("control flow just before rendering")
    return render(request, 'base/delete.html', context)


# def nav(request):
#    return render(request,'navbar.html')

# rooms = [
#     {'id':1, "name": "let's learn python"},
#     {'id':2, "name": "let's learn C++"},
#     {'id':3, "name": "let's learn java"},
# ]
# house = [
#     {'id':1, "name": "let's learn pyth"},
#     {'id':2, "name": "let's learn C"},
#     {'id':3, "name": "let's learn jav"},
# ]
