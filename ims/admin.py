from django.contrib import admin
from ims.models import IMSAddress, IMSInventory, IMSInventoryTransaction

admin.site.register(IMSAddress)
admin.site.register(IMSInventory)
admin.site.register(IMSInventoryTransaction)