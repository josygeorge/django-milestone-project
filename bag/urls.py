from django.urls import path
from . import views


urlpatterns = [
    path('', views.bag, name='bag'),
    path('add_bag/<int:product_id>/', views.add_bag, name='add_bag'),
    path('remove_bag/<int:product_id>/', views.remove_bag, name='remove_bag'),
    path('remove_bag_item/<int:product_id>/', views.remove_bag_item, name='remove_bag_item'),
]
