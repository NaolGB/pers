from django.contrib import admin
from .models import HMSProduct, HMSStockTransaction, HMSWarehouse

admin.site.register(HMSProduct)
admin.site.register(HMSStockTransaction)
admin.site.register(HMSWarehouse)

