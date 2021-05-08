from . import views
from django.urls import path

urlpatterns = [
    path('register-face', views.register_face, name= "register_face"),
    path('register-user', views.register_user, name= "register_user"),
    path('get-names', views.get_names, name="get_names"),
    path('get-name', views.get_name, name="get_name"),
]
