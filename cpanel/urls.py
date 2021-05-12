from . import views
from django.urls import path

urlpatterns = [
    path('detections', views.Detections, name="cpanel-detections"),
    path('detections/<int:user>', views.Detections, name="cpanel-detections"),
    path('detections/<int:user>/<str:date>', views.Detections, name="cpanel-detections"),
    path('', views.Index, name="cpanel-index"),
    path('users/<str:date>', views.Users, name="cpanel-users"),
    path('user/<int:pk>', views.User, name = "cpanel-user"),
    path('update/<int:pk>', views.Update, name = "cpanel-update"),
    path('login', views.loginview, name = "login"),
    path('logout', views.logoutview, name = "logout")
]
