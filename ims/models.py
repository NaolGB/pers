import uuid
from django.db import models
from user_management.models import Company
from django.contrib.auth.models import User

def generate_case_id():
    case_id = uuid.uuid4()
    return case_id

class IMSTransactionType(models.TextChoices):
    CHECKOUT = 'CKO', 'ወጪ'
    CHECKIN = 'CKI', 'ገቢ'
    MOVE = 'MOV', 'ዝውው'
    RESTOCK = 'RTK', 'ተጨማሪ ገቢ ተደርጓል'

class IMSAddress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    location = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.name
    
class IMSInventory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50)
    address = models.ForeignKey(IMSAddress, on_delete=models.PROTECT)
    quantity_on_hand = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    unit_price_estimate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.name} - {self.sku}'

    class Meta:
        unique_together = ('name', 'sku', 'address')
    
class IMSInventoryTransaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction_id = models.UUIDField(editable=False)
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(IMSInventory, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    transaction = models.CharField(
        max_length=3,
        choices=IMSTransactionType.choices,
        default=IMSTransactionType.CHECKOUT
    )
    # source = models.ForeignKey(IMSAddress, on_delete=models.PROTECT, related_name='ims_transaction_source')
    destination = models.ForeignKey(IMSAddress, on_delete=models.PROTECT, related_name='ims_transaction_destination')
    quantity = models.FloatField()

    def __str__(self):
        return f"{self.item} -> {self.destination} | {self.transaction}"
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__gte=0),
                name='ims_transaction_positive_float_value'
            )
        ]