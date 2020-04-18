from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    my_dict = {'insert_temp': "This is from views.py"}
    return render(request,'poisense_app/untitled-1.html',context=my_dict)

def help(request):
    my_help = {'insert_help': "Help page"}
    return render(request,'poisense_app/help.html',context=my_help)
