from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("extract/", AudioToTextAPIView.as_view(), name="extract"),
]
