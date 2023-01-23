from django.shortcuts import render,redirect
from .models import Room, Topic
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
#from django.http import HttpResponse

#template inheritence
# use {% include 'nav.html' %} over all htmls to inherit its properties
# now the inheritence part, use main as the structure of the html file with blocks extending the main.html when they are called. 

def loginPage(request):

    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        try:  #to check if the user even exists
            user=User.objects.get(username=username)
        except:
            messages.error(request, 'User doesn\'t exist')

        user=authenticate(request, username=username, password=password)  

        if user is not None:
            login(request, user)  
            return redirect('home')
        else:
            messages.error(request, 'Username or password doesn\'t exist')


    context={}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    #print("Logout Testing")
    logout(request) #this will basically delete the session id and hence the cookie won't work and will be deleted?
    return redirect('home')

def home(request): #request object is http object which tells us the kind of request method is sent and the kind of data that is being sent as a request
    #return HttpResponse("Home page")
    q=request.GET.get('q')

    if q!=None:

        rooms=Room.objects.filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q) 
            #Q(host__name__icontains=q) 
            
        )
    else:
        rooms=Room.objects.filter()
    room_count=rooms.count() #slower version is len(rooms) since rooms is basically a list of dictionaries after all
    topic=Topic.objects.all()
    context = {"rooms":rooms, "topic": topic, "room_count": room_count}
    return render(request, 'base/home.html', context)

def room(request, pk):
    #return HttpResponse("ROOM")    

    
    room=Room.objects.get(id=pk) #i don't understand why is integer matching with string.. is it converting internally?
    # for i in rooms:
    #     if i.id==int(pk):
    #         room=i        
    #         context={"room":room}
    #The above also woks
    context={"room":room}

    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request):

    form = RoomForm()
    
    if(request.method=='POST'):
      
        form=RoomForm(request.POST) #as far as i understood, the form will extract the values from the request sent by the form.html upon last createRoom call
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request, 'base/room_form.html',context)   

def updateRoom(request,pk):

    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room) #form is filled up with the id=pk data in room table.
    
    if(request.method=='POST'):
        
        form=RoomForm(request.POST, instance=room) #as far as i understood, the form will extract the values from the request sent by the form.html upon last createRoom call
        if form.is_valid():
            form.save()
            return redirect('home')   

    context={'form':form}
    return render(request,'base/room_form.html',context)

def deleteRoom(request,pk):
    #print("delete room views is entered")
    room=Room.objects.get(id=pk)
    context={"obj":room}
    if request.method=='POST':
        room.delete()
        return redirect('home')
    #print("control flow just before rendering")    
    return render(request, 'base/delete.html', context)



#def nav(request):
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
