from django.shortcuts import render
from .models import Food
from order.models import Order
import requests
import json
from django.http import HttpResponse
from django.urls import reverse

# Create your views here.
def food_list(request):
    food = Food.objects.all()
    context = {
        "food":food
    }
    return render(request, 'food/index.html',context)


def send_khalti(request,id):
    food = Food.objects.all()
    context = {
        "food":food
    }
    data = Food.objects.get(id=id)
    order = Order.objects.create(
        food = data,
        qty = 1,
        total_price = data.price,
        user = request.user,
        order_status=Order.Orderstatus.INITIATED

    )
    khalti_data = json.dumps({
        "return_url": "http://localhost:8000"+reverse('callback-khalti'),
        "website_url": "https://example.com/",
        "amount": data.price*100,
        "purchase_order_id": str(order.order_id),
        "purchase_order_name": order.title,
        "product_details": [
            {
                "identity": data.id,
                "name": data.name,
                "total_price": data.price * 100,
                "quantity": 1,
                "unit_price": data.price*100,
            }
        ]
    })
    url = "https://a.khalti.com/api/v2/epayment/initiate/"
    headers = {
    'Authorization': 'key ',
    'Content-Type': 'application/json',
}

    response = requests.post(url, headers=headers, data=khalti_data)
    order.pidx = response.json()['pidx']
    order.save()
    context={
        "url":response.json()['payment_url']
    }
    return render(request, 'food/index.html',context)


def callback_khalti(request):
    context= {}
    context['pidx']=request.GET.get('pidx')
    order = Order.objects.get(pidx=request.GET.get('pidx'))
    if request.GET.get('status')=="Completed":
        print("if")
        order.order_status = Order.Orderstatus.SUCCESS
        order.khalti_txn_id = request.GET.get('transaction_id')
    elif request.GET.get('status')=="Pending":
        print("elif")
        order.order_status = Order.Orderstatus.INITIATED
    else:
        print("esle")
        order.order_status = Order.Orderstatus.FAILURE

    order.save()
    context['order']=order
    print("context",context['order'].order_status)


    return render(request, 'food/transaction_detail.html',context)

