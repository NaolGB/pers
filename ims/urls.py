from django.urls import path
from ims import views

urlpatterns = [
    path('add-address/', views.add_address, name='add_address'),
    path('add-inventory/', views.add_inventory, name='add_inventory'),
    path('inventory-list/', views.inventory_list, name='inventory_list'),
    path('restock-inventory/<uuid:inventory_id>/', views.restock_inventory, name='restock_inventory'),
    path('move-inventory/<uuid:inventory_id>/', views.move_inventory, name='move_inventory'),
    path('checkout-inventory/<uuid:inventory_id>/', views.checkout_inventory, name='checkout_inventory'),
]
