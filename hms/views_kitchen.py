from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import Http404
from .models import HMSProduct, HMSTransactionType, HMSStockTransaction, generate_case_id
from .forms import ProductForm, WarehouseForm, TransactionForm
from user_management.models import UserAccessLevel

# user role test
def has_any_role(role_codes):
    def check_roles(user):
        return user.profile.user_roles.filter(code__in=role_codes).exists()
    return user_passes_test(check_roles)

# user access level test
def is_superuser(user):
    return user.profile.access_level == UserAccessLevel.SUPERUSER
def is_poweruser(user):
    return user.profile.access_level == UserAccessLevel.POWER_USER
def is_functional_leader(user):
    return user.profile.access_level == UserAccessLevel.FUNCTIONAL_LEADER
def is_functional_user(user):
    return user.profile.access_level == UserAccessLevel.FUNCTIONAL_USER

@login_required
@user_passes_test(lambda user: is_superuser(user) or is_poweruser(user) or 
                  is_functional_leader(user) or is_functional_user(user))
def kitchen_dashboard(request):
    context = {
        'all_inventory': HMSProduct.objects.all()
    }
    return render(request, 'hms/kitchen_dashboard.html', context)
