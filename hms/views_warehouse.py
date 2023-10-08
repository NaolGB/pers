from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import Http404, HttpResponse
from .models import HMSProduct, HMSTransactionType, HMSStockTransaction, HMSCategory
from .models import generate_case_id, HMSWarehouse
from .forms import ProductForm, WarehouseForm
from user_management.models import UserAccessLevel
from user_management.user_access_control import has_access_level, has_role


@login_required
@user_passes_test(
    lambda user: has_access_level(
        user, [UserAccessLevel.SUPERUSER, UserAccessLevel.POWER_USER])
)
def add_warehouse(request):
    if request.method == 'POST':
        name = request.POST['name']
        location = request.POST['location']
        company = request.user.profile.company

        warehouse = HMSWarehouse.objects.create(
            name=name, location=location, company=company
        )

        return redirect('power_user_dashboard')

    return render(request, 'hms/add_warehouse.html')


@login_required
@user_passes_test(
    lambda user: has_access_level(
        user, [UserAccessLevel.SUPERUSER, UserAccessLevel.POWER_USER, UserAccessLevel.FUNCTIONAL_LEADER])
)
def add_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        company = request.user.profile.company

        category = HMSCategory.objects.create(
            name=name, company=company
        )

        return redirect('power_user_dashboard')

    return render(request, 'hms/add_category.html')

@login_required
@user_passes_test(
    lambda user: has_access_level(user, [UserAccessLevel.SUPERUSER]) or
    (
        lambda user: has_access_level(user, [UserAccessLevel.SUPERUSER, UserAccessLevel.POWER_USER, UserAccessLevel.FUNCTIONAL_LEADER]) and
        has_role(user, ['HMS-WRH', 'HMS-SUR'])
    )
)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            # save product
            product = form.save()

            return redirect('power_user_dashboard')
    else:
        form = ProductForm()

    context = {
        'form': form,
        'company': request.user.profile.company
    }
    return render(request, 'hms/add_product.html', context)


@login_required
@user_passes_test(
    lambda user: has_access_level(user, [UserAccessLevel.SUPERUSER]) or
    (
        lambda user: has_access_level(user, [UserAccessLevel.SUPERUSER, UserAccessLevel.POWER_USER, UserAccessLevel.FUNCTIONAL_LEADER]) and
        has_role(user, ['HMS-WRH', 'HMS-SUR'])
    )
)
def product_list(request):
    """the dashboard for warehouse manager"""
    context = {
        'all_inventory': HMSProduct.objects.all().order_by('-change_request'),
    }
    print(context['all_inventory'])
    return render(request, 'hms/product_list.html', context)


@login_required
@user_passes_test(
    lambda user: has_access_level(user, [UserAccessLevel.SUPERUSER]) or
    (
        lambda user: has_access_level(user, [UserAccessLevel.SUPERUSER, UserAccessLevel.POWER_USER, UserAccessLevel.FUNCTIONAL_LEADER]) and
        has_role(user, ['HMS-WRH', 'HMS-SUR'])
    )
)
def restock_product(request, product_id):
    error_message = None
    success = None
    product = HMSProduct.objects.get(pk=product_id)

    if request.method == 'POST':
        quantity = float(request.POST.get('restock_quantity'))

        if quantity > 0:
            transaction = HMSStockTransaction.objects.create(
                transaction_id=generate_case_id(),
                product=product,
                user=request.user,
                transaction=HMSTransactionType.RESTOCK,
                quantity=quantity
            )

            # Update product quantity
            product.quantity += quantity
            product.save()

            success = 'Product restocked successfully!'

            return redirect('product_list')
        else:
            error_message = "Restock quantity must be positive."

    return render(request, 'hms/restock_form.html', {'product': product, 'error_message': error_message, 'success': success})


@login_required
def request_checkout(request, product_id):
    success = None
    product = HMSProduct.objects.get(pk=product_id)

    if request.method == 'POST':
        quantity = float(request.POST.get('quantity', 0))
        if 0 < quantity <= product.quantity:
            transaction_id = generate_case_id()
            transaction = HMSStockTransaction.objects.create(
                transaction_id=transaction_id,
                description="ወጪ ጥያቄ",
                product=product,
                user=request.user,
                transaction=HMSTransactionType.CHECKOUT_REQUEST,
                quantity=quantity
            )
            # Update product quantity
            product.change_request += 1
            product.save()
            return redirect('kitchen_dashboard')

    return render(request, 'hms/checkout_request_form.html', {'product': product})


@login_required
@user_passes_test(
    lambda user: has_access_level(user, [UserAccessLevel.SUPERUSER]) or
    (
        lambda user: has_access_level(user, [UserAccessLevel.SUPERUSER, UserAccessLevel.POWER_USER, UserAccessLevel.FUNCTIONAL_LEADER]) and
        has_role(user, ['HMS-WRH', 'HMS-SUR'])
    )
)
def product_transaction_list(request, product_id):
    product = HMSProduct.objects.get(pk=product_id)

    # filter by case_id which are not closed
    checkout_request_transactions = HMSStockTransaction.objects.filter(
        product=product,
        transaction=HMSTransactionType.CHECKOUT_REQUEST
    )
    transaction_ids_checkout_request = checkout_request_transactions.values_list(
        'transaction_id', flat=True)
    checkout_approve_deny_transactions = HMSStockTransaction.objects.filter(
        product=product,
        transaction__in=[HMSTransactionType.CHECKOUT_APPROVE,
                         HMSTransactionType.CHECKOUT_DENY]
    )
    filtered_checkout_request_transactions = checkout_request_transactions.exclude(
        transaction_id__in=checkout_approve_deny_transactions.values_list(
            'transaction_id', flat=True)
    )

    context = {
        'product': product,
        'transactions': filtered_checkout_request_transactions,
    }

    return render(request, 'hms/product_transaction_list.html', context)


@login_required
@user_passes_test(
    lambda user: has_access_level(user, [UserAccessLevel.SUPERUSER]) or
    (
        lambda user: has_access_level(user, [UserAccessLevel.SUPERUSER, UserAccessLevel.POWER_USER, UserAccessLevel.FUNCTIONAL_LEADER]) and
        has_role(user, ['HMS-WRH', 'HMS-SUR'])
    )
)
def close_checkout(request, transaction_id):
    checkout_transaction = get_object_or_404(HMSStockTransaction,
                                             transaction_id=transaction_id, transaction=HMSTransactionType.CHECKOUT_REQUEST)

    # save request change
    if request.method == 'POST':
        action = request.POST.get('action')
        transaction_type = None
        if action == 'approve':
            transaction_type = HMSTransactionType.CHECKOUT_APPROVE
        elif action == 'deny':
            transaction_type = HMSTransactionType.CHECKOUT_DENY
        else:
            raise Http404('Invalid action to close checkout.')

        # update product's change_requests count
        checkout_transaction.product.change_request -= 1

        # update product quantity
        if transaction_type == HMSTransactionType.CHECKOUT_APPROVE:
            checkout_transaction.product.quantity -= checkout_transaction.quantity

        new_transaction = HMSStockTransaction.objects.create(
            transaction_id=transaction_id,
            description="Checkout Approved",
            product=checkout_transaction.product,
            transaction=transaction_type,
            quantity=checkout_transaction.quantity,
            user=request.user
        )

        checkout_transaction.product.save()

        return redirect('product_list')

    context = {'transaction': checkout_transaction}
    return render(request, 'hms/approve_or_deny_checkout.html', context)