from django.contrib import admin
from django.urls import path, include
from .views import (
    register_view
)

urlpatterns = [
    path("", register_view, name="register"),
]
