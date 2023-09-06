import pytest
from django.db import IntegrityError, transaction
from django.contrib.auth.models import User
from user_management.models import Company, Department, Profile, UserRole, UserAccessLevel

# validation test
# ===============
def test_company(sample_company):
    # test creation
    assert Company.objects.filter(name='Test Company').exists()

    # test unique company name
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            Company.objects.create(name='Test Company')

    assert Company.objects.filter(name='Test Company').count() == 1

def test_department(sample_department, sample_company):
    # test creation
    assert Department.objects.filter(name='Test Department').exists()

    # test unique company+department name
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            Department.objects.create(name='Test Department', company=sample_company)

    assert Department.objects.filter(name='Test Department').count() == 1

@pytest.mark.django_db
def test_profile(sample_profile, sample_user, sample_uuid, sample_company, sample_department):
    # test creationn
    assert Profile.objects.filter(user=sample_user).exists()
    assert Profile.objects.count() == 1

    # test unique company+employee_id
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            Profile.objects.create(
                user = sample_user,
                employee_id = sample_uuid,
                company = sample_company,
                department = sample_department
            )

    assert Profile.objects.filter(user=sample_user).count() == 1

# load test
# ===============