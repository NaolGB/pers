import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client
from user_management.models import Company, Department, Profile, UserAccessLevel, UserRole
from hms.models import HMSWarehouse, HMSCategory, HMSProduct

@pytest.mark.django_db
def test_add_warehouse_view():
    user = User.objects.create_user(username='testuser', password='testpassword')
    company = Company.objects.create(name='Test Company', creator=user)
    department = Department.objects.create(name='Test Department', company=company)
    profile = Profile.objects.create(user=user, company=company, employee_id='12345', 
                                     department=department, access_level=UserAccessLevel.SUPERUSER)

    client = Client()
    client.login(username='testuser', password='testpassword')

    # Define the data to be posted to the view
    data = {
        'name': 'Warehouse 1',
        'location': 'Location 1',
    }

    # Make a POST request to the view
    response = client.post(reverse('add_warehouse'), data=data, follow=True)

    # Assert that the response redirects to 'power_user_dashboard'
    assert response.status_code == 200  # You can adjust the status code as needed
    assert response.redirect_chain[0][0] == reverse('power_user_dashboard')

    # Check if the warehouse was created
    assert HMSWarehouse.objects.filter(name='Warehouse 1', location='Location 1', company=company).exists()

@pytest.mark.django_db
def test_add_product_view(client):
    user = User.objects.create_user(username='testuser', password='testpassword')
    company = Company.objects.create(name='Test Company', creator=user)
    department = Department.objects.create(name='Test Department', company=company)
    profile = Profile.objects.create(user=user, company=company, employee_id='12345', 
                                     department=department, access_level=UserAccessLevel.FUNCTIONAL_LEADER)
    warehouse = HMSWarehouse.objects.create(name='Test Warehouse', company=company)
    category = HMSCategory.objects.create(name='Test Category')
    role = UserRole.objects.create(app='hms', code='HMS-WRH', name='Warehouse')
    profile.user_roles.add(role)

    client = Client()
    client.login(username='testuser', password='testpassword')

    url = reverse('add_product')  # Replace 'add_product' with the actual URL name

    # Test GET request to the view
    response_get = client.get(url)
    assert response_get.status_code == 200

    # Test POST request to the view with valid form data
    form_data = {
        'name': 'Test Product',
        'sku': 'TEST123',
        'category': category.id,
        'warehouse': warehouse.id,
        'quantity': 10,
    }

    response_post_valid = client.post(url, data=form_data)
    form = response_post_valid.context['form']  # Assuming your form is available in the context
    assert form.is_valid()



#     # Check if the form data is valid
#     assert response_post_valid.status_code == 302  # Expecting a redirect
    
#     # Check if the form is valid

#     response_post_valid = client.post(url, data=form_data)
#     assert response_post_valid.status_code == 302  # Expecting a redirect

#     # Follow the redirect to check if the product is created
#     redirect_url = response_post_valid.url
#     response_redirected = client.get(redirect_url)
#     assert response_redirected.status_code == 200  # Assuming it redirects to a success page

#     # Check if the product is created in the database
#     created_product = HMSProduct.objects.filter(name='Test Product').first()
#     assert created_product is not None
#     assert created_product.sku == 'TEST123'
#     # Add more assertions for other product attributes as needed