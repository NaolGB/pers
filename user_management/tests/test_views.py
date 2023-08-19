import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Departments, Profile, UserAccessLevel, Company

@pytest.mark.django_db
def test_company_signup_view(client):
    user = User.objects.create_user(username='existinguser', password='testpassword')
    response = client.post(reverse('company_signup'), data={
        'username': 'existinguser',
        'password': 'testpassword',
        'company_name': 'New Company',
    })
    assert response.status_code == 200
    assert 'Username already taken' in str(response.content)

    assert not Company.objects.filter(name='New Company').exists()  # Company should not be created
    assert not Departments.objects.filter(name='Superuser').exists()  # Department should not be created
    assert not Profile.objects.filter(user__username='existinguser').exists()  # Profile should not be created

    # Case: Company already exists
    Company.objects.create(name='Existing Company', creator=user)
    response = client.post(reverse('company_signup'), data={
        'username': 'newuser',
        'password': 'testpassword',
        'company_name': 'Existing Company',
    })
    assert response.status_code == 200  # Expect a response as company exists
    assert 'Company name already taken' in str(response.content)
    assert not User.objects.filter(username='newuser').exists()  # User should not be created
    assert not Departments.objects.filter(name='Superuser').exists()  # Department should not be created
    assert not Profile.objects.filter(user__username='newuser').exists()  # Profile should not be created

    # Case: Successful signup
    response = client.post(reverse('company_signup'), data={
        'username': 'newuser',
        'password': 'testpassword',
        'company_name': 'New Company',
    })
    assert response.status_code == 302  # Expect a redirect after successful signup
    assert User.objects.filter(username='newuser').exists()
    assert Company.objects.filter(name='New Company').exists()
    assert Departments.objects.filter(name='Superuser').exists()  # Check for superuser department creation
    assert Profile.objects.filter(user__username='newuser').exists()  # Check for profile creation

@pytest.mark.django_db
def test_user_login_view(client):
    # Create a user, company, department, and a profile
    user = User.objects.create_user(username='testuser', password='testpassword')
    company = Company.objects.create(name='Test Company', creator=user)
    department = Departments.objects.create(name='Test Department', company=company)
    profile = Profile.objects.create(user=user, company=company, employee_id='12345', 
                                     department=department, access_level=UserAccessLevel.SUPERUSER)

    # Test unsuccessful login attempt with incorrect password
    response = client.post(reverse('user_login'), data={
        'username': 'testuser',
        'password': 'wrongpassword',  # Incorrect password
    })
    assert response.status_code == 200
    response_content = response.content.decode('utf-8')
    print(response_content)  # Print the response content for debugging
    assert 'Invalid login credentials' in response_content

    # Test unsuccessful login attempt with non-existent profile
    profile.delete()
    response = client.post(reverse('user_login'), data={
        'username': 'testuser',
        'password': 'testpassword',
    })
    assert response.status_code == 200  # Expect a response indicating login failure
    assert 'User does not have a profile' in str(response.content)
    profile = Profile.objects.create(user=user, company=company, employee_id='12345', department=department)

    # Test successful login and redirection for superuser
    response = client.post(reverse('user_login'), data={
        'username': 'testuser',
        'password': 'testpassword',
    })
    if profile.access_level == UserAccessLevel.SUPERUSER:
        assert response.status_code == 302  # Expect a redirect after successful login
        assert response.url == reverse('create_user')  # Redirect should go to 'create_user' view
    else:
        assert response.status_code == 200  # Expect a successful login response
        assert 'Successful login' in str(response.content)

    # Attempting to logout
    response = client.get(reverse('user_login'))
    assert response.status_code == 302
    assert response.url == reverse('user_login')

@pytest.mark.django_db
def test_create_user_department_profile_view(client):
    # Create a superuser profile
    superuser = User.objects.create_user(username='superuser', password='testpassword')
    company = Company.objects.create(name='Test Company', creator=superuser)
    superuser_department = Departments.objects.create(name='Superuser Department', company=company)
    poweruser_department = Departments.objects.create(name='Poweruser Department', company=company)
    superuser_profile = Profile.objects.create(
        user=superuser,
        company=company,
        employee_id='1',
        department=superuser_department,
        access_level=UserAccessLevel.SUPERUSER
    )

    # Create a non-superuser profile
    user = User.objects.create_user(username='normaluser', password='testpassword')
    Profile.objects.create(
        user=user,
        company=company,
        employee_id='2',
        department = Departments.objects.create(name='Normal User Department', company=company),
        access_level=UserAccessLevel.READ_ONLY
    )
    assert User.objects.filter(username='normaluser').exists()
    assert Profile.objects.filter(employee_id='2', company=company).exists()

    # Test successful case
    client.login(username='superuser', password='testpassword')
    response = client.post(reverse('create_user'), data={
        'department': superuser_department.id,
        'employee_id': '12345',
        'access_level': UserAccessLevel.POWER_USER,
        'username': 'test_power_user_1',
        'password': 'newpassword',
    })
    assert response.status_code == 200  # Expect a successful response
    client.logout()  # Log out the superuser

    # Test non-superuser access case
    client.login(username='normaluser', password='testpassword')
    response = client.post(reverse('create_user'), data={
        'department': poweruser_department.id,
        'employee_id': '54321',
        'access_level': UserAccessLevel.READ_ONLY,
        'username': 'test_power_user_2',
        'password': 'otherpassword',
    })
    assert response.status_code == 302  # Expect a forbidden response
    client.logout()  # Log out the normaluser

    # Log in the superuser again
    client.login(username='superuser', password='testpassword')

    # Test failing case with missing department
    response = client.post(reverse('create_user'), data={
        'employee_id': '12345',
        'access_level': UserAccessLevel.POWER_USER,
        'username': 'test_power_user_4',
        'password': 'newpassword',
    })
    assert response.status_code == 200  # Expect a response, as this is a validation error case
    assert b"Please select an existing department or enter a new department name." in response.content

    # Test failing case with existing employee ID
    response = client.post(reverse('create_user'), data={
        'department': superuser_department.id,
        'employee_id': '12345',  # Duplicate employee ID
        'access_level': UserAccessLevel.SUPERUSER,
        'username': 'test_power_user_5',
        'password': 'newpassword',
    })
    assert response.status_code == 200  # Expect a response, as this is a validation error case
    assert "Employee ID already exists. Please choose a different Employee ID." in str(response.content)

    # Test failing case with existing username
    response = client.post(reverse('create_user'), data={
        'department': superuser_department.id,
        'employee_id': '54321',
        'access_level': UserAccessLevel.SUPERUSER,
        'username': 'superuser',  # Duplicate username
        'password': 'newpassword',
    })
    assert response.status_code == 200  # Expect a response, as this is a validation error case
    assert "Username already exists. Please choose a different username." in str(response.content)