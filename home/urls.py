from django.urls import re_path
from . import views

app_name = 'home'
urlpatterns= [
re_path(r'^$', views.index, name='index'),
re_path('process/', views.process_input_string, name='process_string')]

#references index function in views.py
