# Generated by Django 4.2.4 on 2023-09-08 03:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HMSCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user_management.company')),
            ],
        ),
        migrations.CreateModel(
            name='HMSProduct',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('sku', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('unit_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('quantity', models.FloatField()),
                ('minimum_stock', models.IntegerField(blank=True, null=True)),
                ('change_request', models.IntegerField(default=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hms.hmscategory')),
            ],
        ),
        migrations.CreateModel(
            name='HMSWarehouse',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('location', models.CharField(blank=True, max_length=200, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user_management.company')),
            ],
        ),
        migrations.CreateModel(
            name='HMSStockTransaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('transaction_id', models.UUIDField(editable=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('transaction', models.CharField(choices=[('CHR', 'Checkout Request'), ('CHA', 'Checkout Approved'), ('CHD', 'Checkout Denied'), ('RTK', 'Restocked')], default='RTK', max_length=3)),
                ('quantity', models.FloatField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hms.hmsproduct')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='hmsproduct',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hms.hmswarehouse'),
        ),
        migrations.AddConstraint(
            model_name='hmsstocktransaction',
            constraint=models.CheckConstraint(check=models.Q(('quantity__gte', 0)), name='positive_float_value'),
        ),
        migrations.AlterUniqueTogether(
            name='hmsproduct',
            unique_together={('name', 'sku')},
        ),
    ]