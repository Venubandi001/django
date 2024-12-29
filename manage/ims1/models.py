from django.db import models

# Create your models here.
class Inventory_ims(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    iin = models.CharField(max_length=100, unique=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    quantity_sold = models.IntegerField()
    selling_price = models.IntegerField()
    profit_earned = models.DecimalField(max_digits=10, decimal_places=2)
    revenue = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed=True
        db_table='inventory'
        
class Order_ims(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    item_id = models.ForeignKey(Inventory_ims, on_delete=models.CASCADE,blank=True) #Cascade simultaneously delete or update an entry from both the child and parent table
    quantity = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    orderdttm = models.DateTimeField(auto_now_add=True)
    # orderdttm = models.DateTimeField()
    is_received = models.BooleanField(default=False)
    is_cancel = models.BooleanField(default=False)
    
    class  Meta:
        managed = True #(default) Django will create, modify and manage the database table based on the models fileds and definition
        db_table ="order"
        
        
class Transactions_ims(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    item = models.ForeignKey(Inventory_ims, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    transactiondttm = models.DateTimeField()
    
    class Meta:
        db_table = 'transactions'
        managed = True
        # verbose_name = 'ModelName'
        # verbose_name_plural = 'ModelNames'

