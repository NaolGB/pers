from django.urls import path
from . import views_warehouse, views_kitchen

urlpatterns = [
    # warehouse
    path('warehouse-dashboard/', view=views_warehouse.warehouse_dashboard, name='warehouse_dashboard'),
    path('add-product/', views_warehouse.add_product, name='add_product'),
    path('add-warehouse/', views_warehouse.add_warehouse, name='add_warehouse'),
    path('restock-product/<uuid:product_id>/', views_warehouse.restock_product, name='restock_product'),
    path('request-checkout/<uuid:product_id>/', views_warehouse.request_checkout, name='request_checkout'),
    path('close-checkout/<uuid:case_id>/', views_warehouse.close_checkout, name='close_checkout'),
    path('product/<uuid:product_id>/transactions/', views_warehouse.product_transaction_list, name='product_transaction_list'),

    # kitchen
    path('kitchen-dahshboard/', view=views_kitchen.kitchen_dashboard, name='kitchen_dashboard'),

]
