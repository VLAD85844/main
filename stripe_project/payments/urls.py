from django.urls import path
from . import views

urlpatterns = [
    path('item/<int:id>/', views.item_detail, name='item_detail'),
    path('buy/<int:id>/', views.create_checkout_session_for_item, name='create_checkout_session'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('buy/order/<int:order_id>/', views.create_checkout_session_for_order, name='create_order_session'),
    path('create-payment-intent/<int:id>/', views.create_payment_intent_for_item, name='create_payment_intent'),
]