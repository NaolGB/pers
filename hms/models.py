import uuid
from django.db import models
from django.contrib.auth.models import User
from user_management.models import Company

def generate_case_id():
    case_id = uuid.uuid4()
    return case_id

class HMSTransactionType(models.TextChoices):
    CHECKOUT_REQUEST = 'CHR', 'Checkout Request'
    CHECKOUT_APPROVE = 'CHA', 'Checkout Approved'
    CHECKOUT_DENY = 'CHD', 'Checkout Denied'
    RESTOCK = 'RTK', 'Restocked'

class HMSWarehouse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    location = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

class HMSCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.name

class HMSProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, blank=True, null=True)
    category = models.ForeignKey(HMSCategory, on_delete=models.PROTECT)
    description = models.TextField(blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    warehouse = models.ForeignKey(HMSWarehouse, blank=False, on_delete=models.PROTECT)
    quantity = models.FloatField()
    minimum_stock = models.IntegerField(blank=True, null=True)
    change_request = models.IntegerField(default=0)

    class Meta:
        unique_together = ('name', 'sku')

    def __str__(self):
        return self.name

class HMSStockTransaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case_id = models.UUIDField(editable=False)
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(HMSProduct, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    transaction = models.CharField(
        max_length=3,
        choices=HMSTransactionType.choices,
        default=HMSTransactionType.RESTOCK
    )
    quantity = models.FloatField()

    def __str__(self):
        return f"{self.transaction} - {self.product} - {self.quantity}"
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__gte=0),
                name='positive_float_value'
            )
        ]