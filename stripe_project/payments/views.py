import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Item, Order


stripe.api_key = settings.STRIPE_SECRET_KEY


def item_detail(request, id):
    item = get_object_or_404(Item, id=id)
    publishable_key = settings.STRIPE_PUBLISHABLE_KEY
    context = {
        'item': item,
        'stripe_publishable_key': publishable_key,
    }
    return render(request, 'payments/item.html', context)


@csrf_exempt
def create_checkout_session_for_item(request, id):
    item = get_object_or_404(Item, id=id)
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': item.currency,
                        'product_data': {
                            'name': item.name,
                            'description': item.description,
                        },
                        'unit_amount': int(item.price * 100),
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=request.build_absolute_uri('/success/'),
            cancel_url=request.build_absolute_uri('/cancel/'),
        )
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'payments/order.html', {'order': order})


@csrf_exempt
def create_checkout_session_for_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    line_items = []
    for order_item in order.orderitem_set.all():
        line_items.append({
            'price_data': {
                'currency': order_item.item.currency,
                'product_data': {
                    'name': order_item.item.name,
                },
                'unit_amount': int(order_item.item.price * 100),
            },
            'quantity': order_item.quantity,
        })
    discounts = []
    tax_rates = []
    if hasattr(order, 'discount'):
        coupon = stripe.Coupon.create(
            percent_off=float(order.discount.percent_off),
            duration='once',
            name=order.discount.name,
        )
        discounts.append({'coupon': coupon.id})
    if hasattr(order, 'tax'):
        tax_rate = stripe.TaxRate.create(
            display_name=order.tax.display_name,
            percentage=float(order.tax.percentage),
            inclusive=order.tax.inclusive,
        )
        tax_rates.append(tax_rate.id)
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            discounts=discounts if discounts else None,
            automatic_tax={'enabled': bool(tax_rates)},
            mode='payment',
            success_url=request.build_absolute_uri('/success/'),
            cancel_url=request.build_absolute_uri('/cancel/'),
        )
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def create_payment_intent_for_item(request, id):
    item = get_object_or_404(Item, id=id)
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(item.price * 100),
            currency=item.currency,
            metadata={'item_id': item.id},
        )
        return JsonResponse({
            'clientSecret': intent.client_secret
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)