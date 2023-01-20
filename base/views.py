from django.shortcuts import render

# Create your views here.
#from django.http import HttpResponse

#template inheritence
# use {% include 'nav.html' %} over all htmls to inherit its properties
# now the inheritence part, use main as the structure of the html file with blocks extending the main.html when they are called. 

def home(request): #request object is http object which tells us the kind of request method is sent and the kind of data that is being sent as a request
    #return HttpResponse("Home page")
    context = {"rooms":rooms}
    return render(request, 'base/home.html', context)

def room(request):
    #return HttpResponse("ROOM")    
    return render(request, 'base/room.html')

#def nav(request):
#    return render(request,'navbar.html')    

rooms = [
    {'id':1, "name": "let's learn python"}, 
    {'id':2, "name": "let's learn C++"}, 
    {'id':3, "name": "let's learn java"}, 
]