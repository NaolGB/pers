import pytest
from django.db.utils import IntegrityError
from hms.models import HMSProduct, HMSStockTransaction, HMSTransactionType

# validation test
# ===============
@pytest.mark.django_db
def test_create_duplicate_product(sample_warehouse, sample_category, sample_product):
    with pytest.raises(IntegrityError):
        HMSProduct.objects.create(
            name="Sample Product",
            sku="SP001",
            category=sample_category,
            warehouse=sample_warehouse,
            quantity=100
        )

@pytest.mark.django_db
def test_create_stock_transaction_with_negative_quantity(sample_product, sample_user,
                                                          sample_uuid):
    with pytest.raises(IntegrityError):
        HMSStockTransaction.objects.create(
            transaction_id=sample_uuid,
            product=sample_product,
            user=sample_user,
            transaction=HMSTransactionType.RESTOCK,
            quantity=-10
        )

# load test
# =========