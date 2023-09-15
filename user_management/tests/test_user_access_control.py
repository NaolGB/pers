import pytest
from django.contrib.auth.models import User
from user_management.models import Department, Profile, UserAccessLevel, Company, UserRole
from user_management.user_access_control import has_access_level, has_role

@pytest.mark.django_db
def test_access_level():
    # test SUPERUSER access_level
    user = User.objects.create_user(username='testuser', password='testpassword')
    company = Company.objects.create(name='Test Company', creator=user)
    department = Department.objects.create(name='Test Department', company=company)
    profile = Profile.objects.create(user=user, company=company, employee_id='12345', 
                department=department, access_level=UserAccessLevel.SUPERUSER)

    assert has_access_level(user, [UserAccessLevel.SUPERUSER]) == True
    assert has_access_level(user, [UserAccessLevel.FUNCTIONAL_USER]) == False

    # test FUNCTIONAL_USER access_level
    profile.access_level = UserAccessLevel.FUNCTIONAL_USER
    assert has_access_level(user, [UserAccessLevel.SUPERUSER]) == False
    assert has_access_level(user, [UserAccessLevel.FUNCTIONAL_USER]) == True

@pytest.mark.django_db
def test_has_role():
    # test has 'HMS-WRH' role
    warehouse_role = UserRole.objects.create(app='hms', code='HMS-WRH', name='Warehouse')
    kitchen_role = UserRole.objects.create(app='hms', code='HMS-KCN', name='Kitchen')
    unassigned_role = UserRole.objects.create(app='hms', code='HMS-UAN', name='Unassigned')

    user = User.objects.create_user(username='testuser', password='testpassword')
    company = Company.objects.create(name='Test Company', creator=user)
    department = Department.objects.create(name='Test Department', company=company)
    profile = Profile.objects.create(user=user, company=company, employee_id='12345', 
                department=department, access_level=UserAccessLevel.FUNCTIONAL_USER)
    
    profile.user_roles.add(warehouse_role)
    assert has_role(user, ['HMS-WRH']) == True
    assert has_role(user, ['HMS-KCN']) == False

    # test has 'HMS-KCN' role
    profile.user_roles.add(kitchen_role)
    assert has_role(user, ['HMS-KCN']) == True
    assert has_role(user, ['HMS-UAN']) == False


    # test has both 'HMS-WRH' and 'HMS-KCN' role
    assert has_role(user, ['HMS-WRH']) == True
    assert has_role(user, ['HMS-KCN']) == True
    assert has_role(user, ['HMS-UAN']) == False
