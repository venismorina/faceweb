from django.shortcuts import render, redirect
from django.http import HttpResponse
import calendar
from sendreq.functions import *
from datetime import date
from sendreq.models import Detection , myUser
from .forms import *

# Create your views here.




def Detections(request, user = None, date = None):
    detections = Detection.objects.all()
    title = "Detections"

    if user != None:
        detections = Detection.get_by_user_id(user)
        title += ": " + myUser.objects.get(pk=user).name
        if date != None:
            detections = Detection.get_by_date(user,date)
            day = date.split("-")[2]
            if int(day) < 10:
                x = day[0]
                day = "0"
                day += x
                date = date[0:-1] + day
            title += " | " + datetime.strftime(datetime.strptime(date, "%Y-%m-%d"), "%d %b,%Y")
    
    context = { "detections" : detections.order_by("-pk"), "title": title }

    return render(request, 'cpanel/detections.html', context)






def Index(request):
    year = datetime.now().year
    month = datetime.now().month
    if month < 10:
        month_year = str(year) + "-0" + str(month)
    else:
        month_year = str(year) + "-" + str(month)

    if request.POST:
        month_year = request.POST['month']
        month = int(month_year.split("-")[1])
        year = int(month_year.split("-")[0])
    
    data = []

    weeks = calendar.monthcalendar(year, month)
    
    for days in weeks:
        week = {}
        i = 0
        for day in days:
            i += 100
            if day == 0:
                week[i] = "0"
            else:
                week[day] = myUser.day_color(date(year, month, day))
        data.append(week)

    context = {"data" : data, "month" : month_year, "title" : "Home"}
    
    #print (data)
    return render(request, 'cpanel/index.html', context)






def Users(request, date):
    users = myUser.objects.all()
    title = "Users"
    title += " | " + datetime.strftime(datetime.strptime(date, "%Y-%m-%d"), "%d %b,%Y")
    context = {"users" : users, "date": date, "title": title }

    return render(request, 'cpanel/users.html', context)






def User(request,pk):
    user = myUser.objects.filter(pk=pk).first()

    title = user.name

    year = datetime.now().year
    month = datetime.now().month
    if month < 10:
        month_year = str(year) + "-0" + str(month)
    else:
        month_year = str(year) + "-" + str(month)

    if request.POST:
        month_year = request.POST['month']
        month = int(month_year.split("-")[1])
        year = int(month_year.split("-")[0])
    
    data = []

    weeks = calendar.monthcalendar(year, month)
    
    for days in weeks:
        week = {}
        i = 0
        total = timedelta(0)  
        for day in days:
            i += 100
            if day == 0:
                week[i] = "0"
            else:
                time = user.today_time(date(year, month, day))
                week[day] = time
                total = total + timedelta(hours=int(time.split(":")[0]), minutes=int(time.split(":")[1]), seconds=int(time.split(":")[2]))
        week["Total"] = str(total)
        data.append(week)

    context = {"data" : data, "user" : user, "month" : month_year, "title": title }

    #print (data)

    return render(request, 'cpanel/user.html', context)


def Update(request,pk):
    user = myUser.objects.filter(pk=pk).first()

    if request.method == "POST":
        form = UpdateForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            dentist = form.save()
            dentist.save()
            return redirect('../users/' + str(date.today()))
    else:
        form = UpdateForm(instance = user)

    context={
        'form': form
    }
   

    return render(request, 'cpanel/update.html', context)


