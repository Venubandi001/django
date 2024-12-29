from django import forms
from .models import Inventory_ims, Order_ims, Transactions_ims

class InventoryForm(forms.ModelForm):
    profit_earned = forms.DecimalField(widget=forms.HiddenInput(), required=False)  # Hidden field
    iin = forms.CharField(required=True)# while editing this values is not geting because we gendrageting unique value so while editing also do the same
    quantity_sold = forms.IntegerField(initial=0)
    revenue = forms.DecimalField(initial=0.0)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set the initial value for the "iin" field
        last_iin_value = Inventory_ims.objects.last()
        if last_iin_value and last_iin_value.iin.isdigit():
            next_iin_value = str(int(last_iin_value.iin) + 1).zfill(4)
        else:
            next_iin_value = "0000"

        # Set the initial value for the 'iin' field
        self.fields['iin'].initial = next_iin_value

    class Meta:
        model = Inventory_ims
        fields = ['id', 'name', 'iin', 'cost', 'quantity', 'quantity_sold', 'selling_price', 'profit_earned', 'revenue']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your name'}),
            'iin': forms.TextInput(attrs={'required': 'required'}),  # Correct the typo 'requried' to 'required'
            'cost': forms.NumberInput(attrs={'placeholder': 'Enter the cost'}),
            'quantity': forms.NumberInput(attrs={'placeholder': 'Select Quantity'}),
            'quantity_sold': forms.NumberInput(attrs={'placeholder': 'Quantity sold'}),
            'selling_price': forms.NumberInput(attrs={'placeholder': 'Select the selling price'}),
            'revenue': forms.NumberInput(attrs={'placeholder': 'Select the revenue'}),
        }

    
       

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order_ims
        exclude = ['orderdttm']
        fields = ['name','item_id','quantity','is_received','is_cancel']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transactions_ims
        fields = ['id','name','item','quantity','selling_price','transactiondttm']
