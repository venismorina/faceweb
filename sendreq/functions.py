from datetime import datetime
from datetime import timedelta


def str_to_time(time):
    return datetime.strptime(time, "%H:%M:%S")

def time_to_str(time):
    return datetime.strftime(time, "%H:%M:%S")

def str_to_date(time):
    return datetime.strptime(time, "%YY/%m/%d")

def date_to_str(time):
    return datetime.strftime(time, "%YY/%m/%d")

def cal_to_time(time):
    return datetime.strftime(time, "%YY-%m-%d")    

def time_to_float(time, datetime = False):
    #print(time)
    if datetime:
        time = time_to_str(time)
    return float(time.replace(":",""))
    






