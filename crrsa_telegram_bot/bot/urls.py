from django.urls import path
from .views import webhook, home

urlpatterns = [
    path('', home),
    path('bot/', webhook),
]
