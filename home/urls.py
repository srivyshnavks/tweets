from django.conf.urls import url
from . import views
from django.urls import path

app_name = 'home'
urlpatterns= [
url(r'^$', views.index, name='index'),
path('process/', views.process_input_string, name='process_string')]



#references index function in views.py
