from django.urls import path

from . import views

urlpatterns = [
    path('addresses/', views.addresses, name='address_list'),
    path('addresses/<int>/', views.addresses,
         name='address_detail')
]
