from django.urls import path

from . import views

# Implementation with generic views system
app_name = "catalog"
urlpatterns = [
    path("triangle/", views.calc_hypotenuse, name="triangle"),
]
