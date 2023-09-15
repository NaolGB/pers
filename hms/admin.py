from django.contrib import admin
from .models import HMSProduct, HMSStockTransaction, HMSWarehouse, HMSCategory

admin.site.register(HMSProduct)
admin.site.register(HMSStockTransaction)
admin.site.register(HMSWarehouse)
admin.site.register(HMSCategory)

