from decimal import Decimal
from django.db.models import Sum
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .forms import InventoryForm, OrderForm, TransactionForm
from .models import Inventory_ims, Order_ims, Transactions_ims
import json
from django.conf import settings


def create_inventory(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        print(form.is_valid())
        if form.is_valid(): #if the  form.is_valid false or true (if false the data not store in database)
            cost = float(form.cleaned_data['cost'])
            quantity = int(form.cleaned_data['quantity'])
            selling_price = float(form.cleaned_data['selling_price'])
            if selling_price >= cost:
                profit_earned = (selling_price * quantity) - (cost * quantity)

                # Create and save the inventory object with profit_earned
                inventory = form.save(commit=False)
                inventory.profit_earned = profit_earned
                inventory.save()

                return redirect('success')  # Redirect to a success page
            else:
                # Add a custom error to the "selling_price" field
                form.add_error('selling_price', 'Selling price must be greater than or equal to cost.')

    else:
        form = InventoryForm()
    return render(request, 'create_inventory.html', {'form': form})




def success_view(request):
    # Your logic for the success page
    context = {
        'message': 'Your action was successful!'
    }
    return render(request, 'success.html', context)




# retrieving data from inventory table
def display_inventory(request):
    inventory_items = Inventory_ims.objects.all()
    return render(request, 'display_inventory.html', {'inventory_items': inventory_items})

# retrieving data from the Transactions table
def display_transactions(request):
    transactions = Transactions_ims.objects.all()  # Retrieve all transactions
    return render(request, 'transactions.html', {'transactions': transactions})

# retrieving data from data from oder table
def orders_received(request):
    received_orders = Order_ims.objects.all()
    return render(request, 'orders_received.html',{'received_orders': received_orders})

# Editing  the inventory list for particular id details
def edit_inventory(request, pk):
    item = get_object_or_404(Inventory_ims, pk=pk)
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=item)
        print(form.is_valid())
        if form.is_valid():
            cost = float(form.cleaned_data['cost'])
            selling_price = float(form.cleaned_data['selling_price'])
            if selling_price >= cost:
                item.profit_earned = 0
                form.save()
                return redirect('display_inventory')  # Redirect to  display_inventory page 
            else:
                # Adding a custom error to the "selling_price" field
                form.add_error('selling_price', 'Selling price must be greater than or equal to cost.')
            
        else:
            print(form.errors)
    else:
        # Get the last previous value for iin from the database
        last_iin_value = Inventory_ims.objects.last()
        # Set the initial value for the 'iin' field
        initial_iin_value = last_iin_value.iin if last_iin_value else "0000"
        form = InventoryForm(instance=item, initial={'iin': item.iin})
        # Use the initial value when creating the form
        form = InventoryForm(instance=item, initial={'iin': initial_iin_value})
    return render(request, 'edit_inventory.html', {'item': item, 'form': form})

# Selling the particular id that will insert in the Transaction table and calculated based on the quantity_sold profit and revenue
def sell_item(request, pk):
    item = get_object_or_404(Inventory_ims, pk=pk)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, initial={'selling_price': item.selling_price})
        quantity_sold = int(request.POST['quantity_sold'])
        selling_price = Decimal(request.POST['selling_price'])
        
        if quantity_sold <= item.quantity:  # Check if quantity_sold is less than or equal to available quantity
            # Calculating profit and revenue
            cost_price = item.cost
            revenue = Decimal(quantity_sold) * selling_price
            
            profit_earned =  (selling_price*(Decimal(quantity_sold))) -(cost_price*(Decimal(quantity_sold)))
            
            item.quantity_sold += quantity_sold
            item.profit_earned += profit_earned
            item.revenue += revenue
            item.quantity -= quantity_sold
            item.save()
            # Creating a transaction record
            transaction = Transactions_ims(name=item.name,item=item,quantity=quantity_sold,
                selling_price=selling_price,
                transactiondttm=timezone.now(),
            )
            transaction.save()
            
            return redirect('success')
        else:
            # Handle the case where quantity_sold is greater than available quantity
            form.add_error('quantity', 'Quantity sold cannot exceed available quantity.')
    else:
        form = TransactionForm(initial={'selling_price': item.selling_price})
    
    return render(request, 'sell_item.html', {'item': item, 'form': form})

# order is placing 
def create_order(request, pk):
    item = get_object_or_404(Inventory_ims, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.item_id = item
        
            # form.save()
            order.cost = item.cost * order.quantity
            order.save()
            # item.quantity -= order.quantity
            item.save()
            
            return redirect('success')
        else:
            print(form.errors)
    else:
        form = OrderForm(initial={'item_id':item.id,'name':item.name, 'cost':item.cost})
    return render(request, 'create_order.html',{'form':form,  'item': item})
            
# in inventory the list shows the details of particular id
def view_item(request, pk):
    item = get_object_or_404(Inventory_ims, id=pk)
    context = {'item': item}
    return render(request, 'view_item.html', context)


# the functionality for deleting the item
def delete_inventory(request, pk):
    item = get_object_or_404(Inventory_ims, pk=pk)
    
    if request.method == 'POST':
        item.delete()
        return redirect('display_inventory')  

    return render(request, 'delete_inventory.html', {'item': item})



def toggle_receive_cancel(request, order_id, action):
    order = get_object_or_404(Order_ims, pk=order_id)

    if action == 'receive':
        # Toggle is_received to True
        order.is_received = not order.is_received
        order.is_cancel = False
        order.save()

        if order.is_received:
            # If received, update the corresponding inventory item's quantity
            inventory_item = order.item_id
            inventory_item.quantity += order.quantity
            inventory_item.save()

    elif action == 'cancel':
        # Toggle is_received to False
        order.is_cancel = not order.is_cancel
        order.is_received = False
        order.save()

    return redirect('success')



# Received orders list printing
def received_orders(request):
    received_orders = Order_ims.objects.filter(is_received=True)
    return render(request, 'received_orders.html', {'received_orders': received_orders})


# printing list of orders canceled 
def canceled_orders(request):
    canceled_orders = Order_ims.objects.filter(is_cancel=True)
    return render(request, 'canceled_orders.html', {'canceled_orders': canceled_orders})


def statistics_view(request):
    total_profit = Inventory_ims.objects.aggregate(total_profit=Sum('profit_earned'))['total_profit'] 
    total_items_in_stock = Inventory_ims.objects.aggregate(total_items_in_stock=Sum('quantity'))['total_items_in_stock']
    item_with_highest_cost = Inventory_ims.objects.order_by('-cost').first()
    item_with_highest_profit = Inventory_ims.objects.order_by('-profit_earned').first()
    item_most_sold = Inventory_ims.objects.order_by('-quantity_sold').first()
    items_out_of_stock = Inventory_ims.objects.filter(quantity=0).count()
    item_with_highest_profit_earned = Inventory_ims.objects.order_by('-profit_earned').first()

    return render(request, 'statistics.html', {
        'total_profit': total_profit,
        'total_items_in_stock': total_items_in_stock,
        'item_with_highest_cost': item_with_highest_cost,
        'item_with_highest_profit': item_with_highest_profit,
        'item_most_sold': item_most_sold,
        'items_out_of_stock': items_out_of_stock,
        'item_with_highest_profit_earned': item_with_highest_profit_earned,
    })


# management.json = settings.MEEDIA_ROOT /''

#ending..............