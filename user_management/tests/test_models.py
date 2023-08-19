import pytest
from django.contrib.auth.models import User
from ..models import Company, Departments, Profile, UserAccessLevel


@pytest.mark.django_db
def test_company_model():
    user = User.objects.create_user(username='testuser', password='testpass')
    company = Company.objects.create(name='Test Company', creator=user)
    
    assert str(company) == 'Test Company'
    assert company.creator == user


@pytest.mark.django_db
def test_departments_model():
    user = User.objects.create_user(username='testuser', password='testpass')
    company = Company.objects.create(name='Test Company', creator=user)
    department = Departments.objects.create(name='Test Department', company=company)
    
    assert str(department) == 'Test Department'
    assert department.company == company


@pytest.mark.django_db
def test_profile_model():
    user = User.objects.create_user(username='testuser', password='testpass')
    company = Company.objects.create(name='Test Company', creator=user)
    department = Departments.objects.create(name='Test Department', company=company)
    profile = Profile.objects.create(user=user, company=company, employee_id='12345', department=department)
    
    assert str(profile) == 'testuser'
    assert profile.company == company
    assert profile.department == department
    assert profile.access_level == UserAccessLevel.READ_ONLY
