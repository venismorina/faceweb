from django.shortcuts import render
from django.http import HttpResponse
from .models import Detection, myUser
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
import json
import base64
from django.core.files.base import ContentFile
from .functions import *
from django import forms
import os

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

@csrf_exempt
def register_face(request):
    if request.method == "POST":
        admin_name = request.POST['admin']
        admin_password = request.POST['password']
        admin = authenticate(username = admin_name, password = admin_password)
        if admin is not None:
            id = request.POST['id']
            image_data = request.POST['image']
            image_name = request.POST['name']
            
            user = myUser.objects.get(id=id)

            if Detection.is_going(user):
                type = 1
            else:
                type = 0

            face = Detection(user = user, type = type)
            face.add_time()
            face.save_date()

            data = ContentFile(base64.b64decode(image_data)) 
            face.image.save(image_name, data, save=True) 
            
            face.save()
            return HttpResponse(json.dumps({"name":user.name, "type":type}))
        else:
            return HttpResponse("Error[2]: Username or Password is wrong!")
    else:
        return HttpResponse("Error[0]: Could Not Register Detection!")


@csrf_exempt
def register_user(request):
    if request.method == "GET":
        admin_name = request.GET['admin']
        admin_password = request.GET['password']
        admin = authenticate(username= admin_name, password=admin_password)
        if admin is not None:
            name = request.GET['name']
            place = request.GET['place']
            user = myUser(name = name, place = place)
            user.save()
            return HttpResponse(user.id)
        else:
            return HttpResponse("Error[2]: Username or Password is wrong!")
    else:
        return HttpResponse("Error[0a]: Could Not Register User!")


@csrf_exempt
def get_names(request):
    if request.method == "GET":
        admin_name = request.GET['admin']
        admin_password = request.GET['password']
        admin = authenticate(username= admin_name, password=admin_password)
        if admin is not None:
            dict = {}
            for user in myUser.objects.all():
                dict[user.id] = user.name
            return HttpResponse(json.dumps(dict))
        else:
            return HttpResponse("Error[2]: Username or Password is wrong!")
    else:
        return HttpResponse("Error[1]: Could Not Get User-Name!")

@csrf_exempt
def get_name(request):
    if request.method == "GET":
        admin_name = request.GET['admin']
        admin_password = request.GET['password']
        admin = authenticate(username= admin_name, password=admin_password)
        if admin is not None:
            id = request.GET['id']
            user = myUser.objects.get(id=id)
            return HttpResponse(user.name)
        else:
            return HttpResponse("Error[2]: Username or Password is wrong!")
    else:
        return HttpResponse("Error[0a]: Could Not Register User!")


@csrf_exempt
def upload_encodings(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                os.remove("static/encodings.pickle")
            except:
                pass
            with open('static/encodings.pickle', 'wb+') as destination:
                for chunk in request.FILES['file'].chunks():
                    destination.write(chunk)
            with open('static/backup/{}.pickle'.format(request.POST['title']), 'wb+') as destination:
                for chunk in request.FILES['file'].chunks():
                    destination.write(chunk)
            return HttpResponse("Encodings uploaded")