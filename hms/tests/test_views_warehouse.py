import pytest
from django.urls import reverse
from django.db import IntegrityError, transaction
from hms.models import HMSWarehouse, HMSProduct, HMSStockTransaction, HMSTransactionType
from django.contrib.auth.models import User
from user_management.models import Profile, UserAccessLevel, UserRole
from hms.views_warehouse import request_checkout, close_checkout
from django.test import RequestFactory


def test_add_warehouse(client, sample_warehouse, sample_company):
    # successful creation and redirect
    warehouse_data = {
        'name': 'New Warehouse',
        'company': sample_company
    }
    respose = client.post(reverse('add_warehouse'), data=warehouse_data)
    assert respose.status_code == 302


def test_add_product(client, sample_product, sample_category, sample_warehouse):
    # successful creation and redirect
    product_data = {
        'name': "Sample Product",
        'sku': "SP002",
        'category': sample_category,
        'warehouse': sample_warehouse,
        'quantity': 100
    }
    respose = client.post(reverse('add_product'), data=product_data)


def test_restock_product(client, sample_product, sample_company, sample_department):
    user = User.objects.create_user(
        username="testuser",
        password="testpassword"
    )
    client.force_login(user)
    profile = Profile.objects.create(
        user=user,
        employee_id='12345',
        company=sample_company,
        department=sample_department,
        access_level=UserAccessLevel.SUPERUSER.value
    )
    user_role = UserRole.objects.create(
        app='hms',  code='HMS-WRH', name='Warehouse')
    profile.user_roles.add(user_role)

    url = reverse('restock_product', args=[sample_product.pk])

    response = client.post(url, {'restock_quantity': '5'})
    assert response.status_code == 302
    assert response.url == reverse('warehouse_dashboard')

    sample_product.refresh_from_db()
    assert sample_product.quantity == 105

    # test negaive quantity
    client.login(username='testuser', password='testpassword')
    response = client.post(url, {'restock_quantity': '-5'})
    assert response.status_code == 200
    assert 'Restock quantity must be positive.' in str(response.content)


def test_request_checkout(client, sample_user, sample_product, request_factory):
    client.force_login(sample_user)

    # Create a request object
    request = request_factory.post(
        reverse('request_checkout', args=[sample_product.pk]),
        data={'quantity': 5}
    )
    request.user = sample_user

    # Call the view function
    response = request_checkout(request, sample_product.pk)

    # Check if the response is a redirect
    assert response.status_code == 302
    assert response.url == reverse('kitchen_dashboard')

    # Check if the product quantity and transaction were updated
    sample_product.refresh_from_db()
    assert sample_product.change_request == 1

    transactions = HMSStockTransaction.objects.filter(
        transaction=HMSTransactionType.CHECKOUT_REQUEST)
    assert transactions.count() == 1
    transaction = transactions.first()
    assert transaction.product == sample_product
    assert transaction.quantity == 5


def test_close_checkout(
    client, sample_company, sample_department, request_factory, sample_checkout_transaction
):
    user = User.objects.create_user(
        username="testuser_closecheckout",
        password="testpassword"
    )
    client.force_login(user)
    profile = Profile.objects.create(
        user=user,
        employee_id='123456',
        company=sample_company,
        department=sample_department,
        access_level=UserAccessLevel.SUPERUSER.value
    )
    user_role = UserRole.objects.create(
        app='hms',  code='HMS-WRH', name='Warehouse')
    profile.user_roles.add(user_role)

    # Create a request object
    request = request_factory.post(
        reverse(
            'close_checkout',
            args=[sample_checkout_transaction.transaction_id]
        )
    )
    request.user = user

    # Create a mutable copy of the POST data
    mutable_post = request.POST.copy()
    mutable_post['action'] = 'approve'
    request.POST = mutable_post

    # Call the view function
    response = close_checkout(request, sample_checkout_transaction.transaction_id)
    assert response.status_code == 302
    assert response.url == reverse('warehouse_dashboard')

    sample_checkout_transaction.refresh_from_db()
    assert HMSStockTransaction.objects.filter(
        transaction=HMSTransactionType.CHECKOUT_APPROVE
        ).filter(transaction_id=sample_checkout_transaction.transaction_id).exists()
    assert HMSStockTransaction.objects.filter(
            transaction=HMSTransactionType.CHECKOUT_REQUEST
        ).filter(transaction_id=sample_checkout_transaction.transaction_id).exists()
