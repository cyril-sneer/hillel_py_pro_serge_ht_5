from django.urls import path

from . import views

# Implementation with generic views system
app_name = "catalog"
urlpatterns = [
    path("triangle/", views.calc_hypotenuse, name="triangle"),
]

urlpatterns += [
    path("person/", views.create_person, name='person'),
    path("person/<int:pk>/", views.update_person, name='person-detail')
]