from django.urls import path

from . import views

urlpatterns = [

    path('collage', views.iiifmanifest)

]