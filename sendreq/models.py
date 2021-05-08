from django.db import models
from .functions import *

class myUser(models.Model):
    
    name = models.CharField(max_length=255)
    CHOICES = (
        (1, 'Prishtine'),
        (2, 'Drenas'),
        (3, 'Ferizaj')
    )
    place = models.IntegerField(choices = CHOICES)
    work_hours = models.CharField(default = "08:00:00", max_length =11)
    
    def __str__(self):
        return f'{self.id} | {self.name} | {self.get_place()}'

    def get_place(self, x=None):
        if x == None:
            x = self.place
        return self.CHOICES[x-1][1]
        #return x
        
    def today_time(self, date = datetime.now()):
        try:
            return Detection.get_last(self, date).work_time
        except:
            return "00:00:00"

    def today_type(self, time = None):
        if time == None:
            time = self.today_time()

        time = time_to_float(time)

        if time == 0:
            return 0
        if time >= time_to_float(self.work_hours) * 0.9:
            return 1
        elif time >= time_to_float(self.work_hours) * 0.6:
            return 2
        else:
            return 3

    def today_time_color(self, time = None):
        if time == None:
            time = self.today_time()
        array = ["secondary","success","warning","danger"]
        return array[self.today_type(time)]
    
    def today_time_color_date(self, date):
        time = self.today_time(date)
        return self.today_time_color(time)
    
    def progress_time(self, time = None):
        if time == None:
            time = self.today_time()
        return int(( time_to_float(time) / time_to_float(self.work_hours) ) * 100)
    
    def progress_time_date(self, date):
        time = self.today_time(date)
        return self.progress_time(time)
    
    def progress_color(self, time = None):
        if time == None:
            time = self.today_time()

        array = ["","green","amber","blush"]
        return array[self.today_type(time)]
    
    def progress_color_date(self, date):
        time = self.today_time(date)
        return self.progress_color(time)

    @classmethod
    def day_color(self, date):
        users = self.objects.all()
        warning = 0
        danger = 0
        none = True
        for user in users:
            type = user.today_type(user.today_time(date))

            if type != 0:
                none = False
                
            if type == 2:
                warning += 1
            if type == 3 or type == 0:
                danger += 1
        
        if none:
            return "secondary"

        if danger > 2 or warning > 8:
            return "danger"
        elif danger > 0 or warning > 2:
            return "warning"
        else:
            return "success"



class Detection(models.Model):
    user = models.ForeignKey(myUser, on_delete=models.CASCADE)
    date = models.DateTimeField(default = None)
    image = models.ImageField(default='default.jpg', upload_to="detections")
    type = models.IntegerField(default = 0)
    work_time = models.CharField(max_length = 11, default = "00:00:00")

    @classmethod
    def is_going(self, user):
        today = datetime.date(datetime.now())
        last_type = self.get_last(user, today);
        if last_type != None:
            if last_type.type == 0:
                return True
        return False
    
    @classmethod
    def get_by_date(self, user, date):
        return self.objects.filter(date__date = date, user = user)

    @classmethod
    def get_by_user_id(self, user):
        return self.objects.filter(user_id = user)

    def save_date(self):
        self.date = datetime.now()
        return True
    
    def add_time(self):
        if self.is_going(self.user):
            time = datetime.now()
            last = self.get_last(self.user)
            last_date = last.date.replace(tzinfo=None)
            self.work_time = time_to_str( str_to_time(last.work_time) + ( time - last_date ) )
            return self.work_time
        else:
            last = self.get_last(self.user)
            try:
                self.work_time = last.work_time
            except:
                pass
            return self.work_time

    @classmethod
    def get_last(self, user, date = datetime.date(datetime.now())):
        return self.objects.filter(date__date = date, user = user).last()
    
    @property
    def type_str(self):
        array = ["Hyrje", "Dalje"]
        return array[self.type]
    
    @property
    def type_color(self):
        array = ["success", "danger"]
        return array[self.type]
        
    def __str__(self):
        return f'{self.user.name} | {self.date}'


# mas ni muji mi trajnnu fotot
# me start si te prek start
# e ujt e ni route ku unesh i nrru sa or ka nejt njeri n pun edhe unesh e uploadu foton tane
