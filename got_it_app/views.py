from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def room(request, room_name):
    context = {'room_name': room_name}
    return render(request, "got_it_app/main.html", context)

def home(request):
    context = {}
    return HttpResponse("HOME")