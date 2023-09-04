import pytest
import uuid
from django.db.utils import IntegrityError
from user_management.models import Company
from hms.models import HMSWarehouse, HMSCategory, HMSProduct, HMSStockTransaction, HMSTransactionType
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

@pytest.fixture
def sample_user():
    return User.objects.create(username="test_user")

@pytest.fixture
def sample_uuid():
    uuid4 = uuid.uuid4()
    return uuid4

@pytest.fixture
def sample_company(sample_user):
    return Company.objects.create(name="Sample Company", creator=sample_user)

@pytest.fixture
def sample_warehouse(sample_company):
    return HMSWarehouse.objects.create(name="Sample Warehouse", company=sample_company)

@pytest.fixture
def sample_category():
    return HMSCategory.objects.create(name="Sample Category")

@pytest.fixture
@pytest.mark.django_db
def sample_product(sample_warehouse, sample_category):
    return HMSProduct.objects.create(
        name="Sample Product",
        sku="SP001",
        category=sample_category,
        warehouse=sample_warehouse,
        quantity=100
    )

@pytest.fixture
@pytest.mark.django_db
def sample_transaction(sample_product, sample_user, sample_uuid):
    return HMSStockTransaction.objects.create(
        case_id=sample_uuid,
        product=sample_product,
        user=sample_user,
        transaction=HMSTransactionType.RESTOCK,
        quantity=50
    )

@pytest.mark.django_db
def test_create_warehouse(sample_warehouse):
    assert sample_warehouse.id is not None

@pytest.mark.django_db
def test_create_category(sample_category):
    assert sample_category.id is not None

@pytest.mark.django_db
def test_create_product(sample_product):
    assert sample_product.id is not None

@pytest.mark.django_db
def test_create_stock_transaction(sample_transaction):
    assert sample_transaction.id is not None

@pytest.mark.django_db
def test_create_duplicate_product(sample_warehouse, sample_category):
    # sample_product fixture is not creating HMSProduct on the mark.django_db so it
    # manually created here for the test
    sample_product = HMSProduct.objects.create(
        name="Sample Product",
        sku="SP001",
        category=sample_category,
        warehouse=sample_warehouse,
        quantity=100
    )
    assert sample_product.id is not None

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
            case_id=sample_uuid,
            product=sample_product,
            user=sample_user,
            transaction=HMSTransactionType.RESTOCK,
            quantity=-10
        )
