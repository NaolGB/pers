import pytest
import uuid
from django.test import RequestFactory
from user_management.models import Company, Department, Profile, UserAccessLevel
from hms.models import HMSWarehouse, HMSCategory, HMSProduct, HMSStockTransaction, HMSTransactionType
from django.contrib.auth.models import User

# user_management
@pytest.fixture
def sample_user(db):
    user = User.objects.create(username="test_user", password='1234')
    return user

@pytest.fixture
def sample_uuid():
    uuid4 = "d631db8d-52fc-4f61-8e3d-440ce971a72d"
    uuid_val = uuid.UUID(uuid4)
    return uuid_val

@pytest.fixture
def sample_company(sample_user, db):
    return Company.objects.create(name="Test Company", creator=sample_user)

@pytest.fixture
def sample_department(sample_company, db):
    return Department.objects.create(name="Test Department", company=sample_company)

@pytest.fixture
def sample_profile(sample_user, sample_uuid, sample_company, sample_department):
    return Profile.objects.create(
        user = sample_user,
        employee_id = sample_uuid,
        company = sample_company,
        department = sample_department,
    )

# hms
@pytest.fixture
def sample_warehouse(sample_company, db):
    return HMSWarehouse.objects.create(name="Sample Warehouse", company=sample_company)

@pytest.fixture
def sample_category(db):
    return HMSCategory.objects.create(name="Sample Category")

@pytest.fixture
def sample_product(sample_warehouse, sample_category, db):
    return HMSProduct.objects.create(
        name="Sample Product",
        sku="SP001",
        category=sample_category,
        warehouse=sample_warehouse,
        quantity=100
    )

@pytest.fixture
def sample_transaction(sample_product, sample_user, sample_uuid, db):
    return HMSStockTransaction.objects.create(
        transaction_id=sample_uuid,
        product=sample_product,
        user=sample_user,
        quantity=50
    )

@pytest.fixture
def sample_checkout_transaction(sample_product, sample_user, sample_uuid, db):
    return HMSStockTransaction.objects.create(
        transaction_id=sample_uuid,
        product=sample_product,
        user=sample_user,
        transaction = HMSTransactionType.CHECKOUT_REQUEST,
        quantity=50
    )

@pytest.fixture
def request_factory():
    return RequestFactory()