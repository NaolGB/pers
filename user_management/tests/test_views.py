import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from user_management.models import Department, Profile, UserAccessLevel, Company

def test_company_signup(client, sample_user, sample_company):
    # Case: username already taken
    response = client.post(
        reverse('company_signup'), 
        data={
            'username': 'test_user', # sample_user has the username test_user
            'password': '1234',
            'company_name': 'New Company',
        }
    )

    assert response.status_code == 200
    assert 'Username already taken' in str(response.content)

    # Case: Company already exists
    response = client.post(
        reverse('company_signup'), 
        data={
        'username': 'newuser',
        'password': 'testpassword',
        'company_name': 'Test Company', # sample_company has the name Test Company
        }
    )

    assert response.status_code == 200
    assert 'Company name already taken' in str(response.content)

    # no record should be created
    assert not Company.objects.filter(name='New Company').exists() 
    assert not User.objects.filter(username='newuser').exists()  # User should not be created
    assert not Department.objects.filter(name='Superuser').exists()  # Department should not be created
    assert not Profile.objects.filter(user__username='newuser').exists()  # Profile should not be created

    # Case: Successful signup
    response = client.post(
        reverse('company_signup'), 
        data={
        'username': 'newuser',
        'password': 'testpassword',
        'company_name': 'New Company',
        }
    )

    assert response.status_code == 302  # redirect
    assert response.url == reverse('user_login')

    assert User.objects.filter(username='newuser').exists()
    assert Company.objects.filter(name='New Company').exists()
    assert Department.objects.filter(name='Superuser').exists()  
    assert Profile.objects.filter(user__username='newuser').exists()

@pytest.mark.django_db
def test_user_login(client, sample_user, sample_profile):
    # Test unsuccessful login attempt with incorrect password
    response = client.post(
        reverse('user_login'), 
        data={
            'username': 'test_user',
            'password': 'wrongpassword',
        }
    )
    assert response.status_code == 200
    assert 'Invalid login credentials' in str(response.content)

    # test successful login

def test_create_user_department_profile_view(client, sample_company, sample_user, sample_profile, sample_department):
    # Create a superuser or power user for testing
    user = User.objects.create_user(
        username="testuser",
        password="testpassword"
    )
    client.force_login(user)
    profile = Profile.objects.create(
        user=user,
        employee_id = '12345',
        company = sample_company,
        department = sample_department,
        access_level=UserAccessLevel.SUPERUSER.value
    )

    # failing case with missing department
    response = client.post(
        reverse('create_user'), 
        data={
            'employee_id': '12345',
            'access_level': UserAccessLevel.POWER_USER,
            'username': 'test_power_user_4',
            'password': 'newpassword',
        }
    )
    assert response.status_code == 200
    assert b"Please select an existing department or enter a new department name." in response.content

    # failing case with existing employee ID
    response = client.post(reverse('create_user'), data={
        'department': sample_department.id,
        'employee_id': '12345',  # Duplicate employee ID
        'access_level': UserAccessLevel.SUPERUSER,
        'username': 'test_power_user_5',
        'password': 'newpassword',
    })
    assert response.status_code == 200  # Expect a response, as this is a validation error case
    assert "Employee ID already exists. Please choose a different Employee ID." in str(response.content)

    # failing case with existing username
    response = client.post(
        reverse('create_user'), 
        data={
            'department': sample_department.id,
            'employee_id': '54321',
            'access_level': UserAccessLevel.SUPERUSER,
            'username': 'testuser',  # Duplicate username
            'password': 'newpassword',
        }
    ) 
    assert response.status_code == 200  
    assert "Username already exists. Please choose a different username." in str(response.content)

    # successful case
    data = {
        'department': sample_department.id,
        'employee_id': '123456789',
        'access_level': UserAccessLevel.POWER_USER.value,
        'username': 'testusername',
        'password': 'testpassword',
    }

    # Simulate a POST request to the view
    response = client.post(reverse('create_user'), data=data)
    print(response.content)
    assert response.status_code == 302  
    assert User.objects.filter(username='testusername').exists()