from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('available-units/', views.available_units, name='available_units'),
    path('charges-import-duty/', views.charges, name='charges'),
    path('contact/', views.contact, name='contact'),
]
