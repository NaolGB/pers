import uuid
from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250, unique=True, blank=False)
    creator = models.OneToOneField(User, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.name

class UserAccessLevel(models.TextChoices):
    # managers, owners, IT heads, department managers
    SUPERUSER = 'SU', 'Superuser/Administrator'
    POWER_USER = 'PU', 'Power User/Manager'

    # non-management individual end user
    # ex: a user requesting to check material out of warehouse
    FUNCTIONAL = 'FN', 'Functional/User Role Access'
    
    # can only see information
    # ex: users tasked with balancing inventory
    READ_ONLY = 'RO', 'Read-Only/User'

    # managers, owners
    REPORTING = 'RP', 'Reporting/User Analytics'

    # others
    EXTERNAL = 'EX', 'External/Supplier/Customer'
    DATA_ENTRY = 'DE', 'Data Entry/Transaction User'
    RESTRICTED = 'RE', 'Restricted Access'
    WORKFLOW = 'WF', 'Workflow/Approval User'
    AUDIT = 'AD', 'Audit/User Activity'

class UserRoles(models.TextChoices):
    # HMS roles
    STORE = 'HMS-STR', 'Store'
    KITCHEN = 'HMS-KCN', 'Kitchen'

class Departments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250, blank=False)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('name', 'company')  # Ensure department name is unique within each company

    def __str__(self):
        return self.name

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    employee_id = models.CharField(max_length=32)
    department = models.ForeignKey(Departments, on_delete=models.PROTECT)
    access_level = models.CharField(
        max_length=2,
        choices=UserAccessLevel.choices,
        default=UserAccessLevel.READ_ONLY,
    )

    class Meta:
        unique_together = ('company', 'employee_id')  # Ensure company and employee_id combination is unique

    def __str__(self):
        return self.user.username