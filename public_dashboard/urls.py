from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("spd/<int:pk>", views.DetailView.as_view(), name="detail"),
]
