# Generated by Django 4.2.4 on 2023-09-17 15:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250, unique=True)),
                ('creator', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=250)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user_management.company')),
            ],
            options={
                'unique_together': {('name', 'company')},
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('app', models.CharField(max_length=20)),
                ('code', models.CharField(max_length=7)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('employee_id', models.CharField(max_length=32)),
                ('access_level', models.CharField(choices=[('SU', 'Superuser/Administrator'), ('PU', 'Manager'), ('FL', 'Team Leader/Supervisor'), ('FN', 'Operational User')], default='FN', max_length=2)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user_management.company')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user_management.department')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('user_roles', models.ManyToManyField(to='user_management.userrole')),
            ],
            options={
                'unique_together': {('company', 'employee_id')},
            },
        ),
    ]
