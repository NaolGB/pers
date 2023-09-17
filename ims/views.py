from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect
from . models import IMSAddress, IMSInventory, IMSTransactionType, IMSInventoryTransaction
from .forms import AddInventoryForm
from .models import generate_case_id
from user_management.models import UserAccessLevel

from user_management.user_access_control import has_access_level, has_role

@login_required
@user_passes_test(
    lambda user: has_access_level(
        user, [UserAccessLevel.SUPERUSER, UserAccessLevel.POWER_USER])
)
def add_address(request):
    if request.method == 'POST':
        name = request.POST['name']
        location = request.POST['location']
        company = request.user.profile.company

        # Create the IMSAddress instance
        IMSAddress.objects.create(name=name, location=location, company=company)
        
        return redirect('power_user_dashboard')  

    return render(request, 'ims/add_address.html')

@login_required
@user_passes_test(
    lambda user: has_access_level(user, [UserAccessLevel.SUPERUSER]) or
    (
        lambda user: has_access_level(user, [UserAccessLevel.SUPERUSER, UserAccessLevel.POWER_USER, UserAccessLevel.FUNCTIONAL_LEADER]) and
        has_role(user, ['IMS-WRH'])
    )
)
def add_inventory(request):
    if request.method == 'POST':
        form = AddInventoryForm(request.POST)
        if form.is_valid():
            inventory_item = form.save()
            return redirect('inventory_list')
    else:
        form = AddInventoryForm()
    
    return render(request, 'ims/add_inventory.html', {'form': form})

@login_required
@user_passes_test(
    lambda user: has_access_level(user, [UserAccessLevel.SUPERUSER, UserAccessLevel.POWER_USER, UserAccessLevel.FUNCTIONAL_LEADER])
)
def inventory_list(request):
    inventory_items = IMSInventory.objects.all()
    context = {'inventory_items': inventory_items}
    return render(request, 'ims/inventory_list.html', context)

@login_required
@user_passes_test(
    lambda user: has_access_level(user, [UserAccessLevel.SUPERUSER]) or
    (
        lambda user: has_access_level(user, [UserAccessLevel.SUPERUSER, UserAccessLevel.POWER_USER, UserAccessLevel.FUNCTIONAL_LEADER]) and
        has_role(user, ['IMS-WRH'])
    )
)
def restock_inventory(request, inventory_id):
    item = IMSInventory.objects.get(pk=inventory_id)

    if request.method == 'POST':
        quantity = float(request.POST.get('restock_quantity'))

        if quantity > 0:
            transaction = IMSInventoryTransaction.objects.create(
                transaction_id=generate_case_id(),
                item=item,
                user=request.user,
                transaction=IMSTransactionType.RESTOCK,
                quantity=quantity,
                destination = item.address
            )

            # Update product quantity
            item.quantity_on_hand += quantity
            item.save()

            return redirect('inventory_list')
        
    return render(request, 'ims/restock_inventory.html', {'inventory_item': item})

@login_required
@user_passes_test(
    lambda user: has_access_level(user, [UserAccessLevel.SUPERUSER]) or
    (
        lambda user: has_access_level(user, [UserAccessLevel.SUPERUSER, UserAccessLevel.POWER_USER, UserAccessLevel.FUNCTIONAL_LEADER]) and
        has_role(user, ['IMS-WRH'])
    )
)
def checkout_inventory(request, inventory_id):
    item = IMSInventory.objects.get(pk=inventory_id)

    if request.method == 'POST':
        quantity = float(request.POST.get('checkout_quantity'))

        if (quantity > 0) and (quantity <= item.quantity_on_hand):
            transaction = IMSInventoryTransaction.objects.create(
                transaction_id=generate_case_id(),
                item=item,
                user=request.user,
                transaction=IMSTransactionType.CHECKOUT,
                quantity=quantity,
                destination = item.address
            )

            # Update product quantity
            item.quantity_on_hand -= quantity
            item.save()

            return redirect('inventory_list')
        
    return render(request, 'ims/checkout_inventory.html', {'inventory_item': item})


@login_required
@user_passes_test(
    lambda user: has_access_level(user, [UserAccessLevel.SUPERUSER]) or
    (
        lambda user: has_access_level(user, [UserAccessLevel.SUPERUSER, UserAccessLevel.POWER_USER, UserAccessLevel.FUNCTIONAL_LEADER]) and
        has_role(user, ['IMS-WRH'])
    )
)
def move_inventory(request, inventory_id):
    source_item = IMSInventory.objects.get(pk=inventory_id)
    # print(destination_address)

    if request.method == 'POST':
        quantity = float(request.POST.get('move_quantity'))
        destination_id = request.POST.get('destination_id')
        destination_address = IMSAddress.objects.get(pk=destination_id)

        if destination_id != source_item.address.id:
            if (quantity > 0) and (quantity <= source_item.quantity_on_hand):
                transaction = IMSInventoryTransaction.objects.create(
                    transaction_id=generate_case_id(),
                    item=source_item,
                    user=request.user,
                    transaction=IMSTransactionType.MOVE,
                    quantity=quantity,
                    destination = destination_address
                )

                # Update inventory source quantity
                source_item.quantity_on_hand -= quantity
                source_item.save()

                # update inventory destination quantity
                try:
                    destination_item = IMSInventory.objects.get(
                        name=source_item.name, sku=source_item.sku, address=destination_address
                    )
                    destination_item.quantity_on_hand += quantity
                    destination_item.save()
                except:
                    new_item = IMSInventory.objects.create(
                        name = source_item.name,
                        sku=source_item.sku,
                        address=destination_address,
                        quantity_on_hand=quantity,
                        description=source_item.description,
                        unit_price_estimate = source_item.unit_price_estimate
                    )

                return redirect('inventory_list')
    
    context = {
        'inventory_item': source_item,
        'destination': IMSAddress.objects.filter(company=request.user.profile.company),
    }

    return render(request, 'ims/move_inventory.html', context)
