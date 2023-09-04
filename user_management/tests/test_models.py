import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from user_management.models import Company, Department, Profile, UserRole, UserAccessLevel

@pytest.mark.django_db
def test_company_creation():
    company = Company.objects.create(name='Test Company', creator=User.objects.create_user(
        'creator', 'creator@example.com', 'password')
        )
    assert str(company) == 'Test Company'

@pytest.mark.django_db
def test_unique_company_name():
    Company.objects.create(name='Test Company', creator=User.objects.create_user(
        'creator', 'creator@example.com', 'password')
        )
    
    with pytest.raises(IntegrityError):
        Company.objects.create(name='Test Company', creator=User.objects.create_user(
            'creator2', 'creator2@example.com', 'password')
            )

@pytest.mark.django_db
def test_department_creation():
    company = Company.objects.create(name='Test Company', creator=User.objects.create_user(
        'creator', 'creator@example.com', 'password')
        )
    department = Department.objects.create(name='Test Department', company=company)
    assert str(department) == 'Test Department'

@pytest.mark.django_db
def test_unique_department_name_within_company():
    company = Company.objects.create(name='Test Company', creator=User.objects.create_user(
        'creator', 'creator@example.com', 'password')
        )
    Department.objects.create(name='Test Department', company=company)
    
    with pytest.raises(IntegrityError):
        Department.objects.create(name='Test Department', company=company)

@pytest.mark.django_db
def test_create_profile():
    company = Company.objects.create(name="Test Company", creator=User.objects.create_user("creator"))
    department = Department.objects.create(name="Test Department", company=company)
    user = User.objects.create_user("testuser", password="testpassword")
    # role = UserRole.objects.create(name=UserRole.RoleChoices.WAREHOUSE)

    profile = Profile.objects.create(
        user=user,
        employee_id="12345",
        company=company,
        department=department,
        access_level=UserAccessLevel.SUPERUSER,
    )
    # profile.role.add(role)

    assert Profile.objects.count() == 1
    assert profile.user == user
    assert profile.employee_id == "12345"
    assert profile.company == company
    assert profile.department == department
    assert profile.access_level == UserAccessLevel.SUPERUSER
    # assert role in profile.role.all()

@pytest.mark.django_db
def test_unique_company_employee_id():
    company = Company.objects.create(name="Test Company", creator=User.objects.create_user("creator"))
    department = Department.objects.create(name="Test Department", company=company)
    user = User.objects.create_user("testuser", password="testpassword")

    profile1 = Profile.objects.create(
        user=user,
        employee_id="12345",
        company=company,
        department=department,
        access_level=UserAccessLevel.SUPERUSER,
    )

    with pytest.raises(IntegrityError):
        profile2 = Profile.objects.create(
            user=user,
            employee_id="12345",
            company=company,
            department=department,
            access_level=UserAccessLevel.SUPERUSER,
        )