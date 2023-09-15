from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import Http404
from .models import HMSProduct, HMSTransactionType, HMSStockTransaction, generate_case_id
from .forms import ProductForm, WarehouseForm, TransactionForm
from user_management.models import UserAccessLevel
from user_management.user_access_control import has_access_level, has_role

@login_required
@user_passes_test(
    lambda user: has_access_level(
        user, 
        [
            UserAccessLevel.SUPERUSER, 
            UserAccessLevel.POWER_USER, 
            UserAccessLevel.FUNCTIONAL_LEADER,
            UserAccessLevel.FUNCTIONAL_USER
        ]
    )
)
def kitchen_dashboard(request):
    context = {
        'all_inventory': HMSProduct.objects.all()
    }
    return render(request, 'hms/request_checkout_product_list.html', context)
