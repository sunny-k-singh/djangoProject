from django.shortcuts import render,redirect
from .models import Room
from .forms import RoomForm
# Create your views here.
#from django.http import HttpResponse

#template inheritence
# use {% include 'nav.html' %} over all htmls to inherit its properties
# now the inheritence part, use main as the structure of the html file with blocks extending the main.html when they are called. 

def home(request): #request object is http object which tells us the kind of request method is sent and the kind of data that is being sent as a request
    #return HttpResponse("Home page")
    rooms=Room.objects.all()
    context = {"rooms":rooms}
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
    print("delete room views is entered")
    room=Room.objects.get(id=pk)
    context={"obj":room}
    if request.method=='POST':
        room.delete()
        return redirect('home')
    print("control flow just before rendering")    
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
