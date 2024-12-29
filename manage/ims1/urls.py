
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('', views.statistics_view, name='inventory'),
    path('create_inventory/', views.create_inventory, name='create_inventory'),
    path('success/', views.success_view, name='success'),
    # path('transactions/<int:pk>/delete/', views.delete_transaction, name='delete_transaction'),  # Delete
    path('display_inventory/', views.display_inventory, name='display_inventory'),# data retrived from inventory table
    path('edit_inventory/<int:pk>/', views.edit_inventory, name='edit_inventory'), # URL for editing an inventory item
    path('sell_item/<int:pk>/', views.sell_item, name='sell_item'),# URL for selling an inventory item
    path('create/order/<int:pk>/', views.create_order, name='create_order'),# URL for creating an order for an item
    path('view_item/<int:pk>/', views.view_item, name='view_item'),#View the particular id details
    path('delete_inventory/<int:pk>/', views.delete_inventory, name='delete_inventory'),
    path('orders_received/', views.orders_received, name='orders_received'),
    path('transactions/', views.display_transactions, name='transactions'),
    path('received_orders/', views.received_orders, name='received_orders'),
    path('canceled_orders/', views.canceled_orders, name='canceled_orders'),
    path('toggle_receive_cancel/<int:order_id>/<str:action>/', views.toggle_receive_cancel, name='toggle_receive_cancel'),

    
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    path('json_file/', serve, {'document_root': settings.STATIC_ROOT, 'path': 'ims1/media/management.json'}),
]