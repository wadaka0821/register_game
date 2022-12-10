from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
import uuid
import json

from .models import Product, Purchase, History

# Create your views here.
def purchase(request, history_id):
    return HttpResponse("This is Purchase Page")

def count_up(request):

    history_id = uuid.UUID(request.POST.get('history_id'))
    product_id = uuid.UUID(request.POST.get('product_id'))
    history = History.objects.get(history_id=history_id)
    product = Product.objects.get(product_id=product_id)

    purchase = history.purchase_set.filter(product_id=product)
    if len(purchase):
        purchase = purchase[0]
        purchase.purchase_num += 1
        purchase.save()
    else:
        history.purchase_set.create(product_id=product, purchase_num=1)
    history.total_price += product.price
    history.total_product += 1
    history.save()

    backet = list()
    total_price = 0
    total_num = 0
    for purchase in history.purchase_set.all():
        tmp_dict = {
            'product_name':purchase.product_id.product_name,
            'price':purchase.product_id.price,
            'purchase_num':purchase.purchase_num,
            'total':purchase.product_id.price * purchase.purchase_num,
        }
        backet.append(tmp_dict)
        total_price += tmp_dict['total']
        total_num += tmp_dict['purchase_num']
    
    backet.append({
        'product_name':'',
        'price':'Total',
        'purchase_num':total_num,
        'total':total_price,
    })
    
    params = {
        'backet':backet,
    }

    json_str = json.dumps(params, ensure_ascii=False, indent=2)
    return HttpResponse(json_str)

def index(request):
    product_list = Product.objects.all()

    history = History(purchase_date=timezone.now(), total_price=0, total_product=0)
    history.save()

    history_id = history.history_id

    purchase_list = list()
    if history.total_product:
        for purchase in Purchase.objects.get(history_id=history_id):
            tmp_dict = {
                'product_name':purchase.product_id.product_name,
                'price':purchase.product_id.price,
                'purchase_num':purchase.purchase_num,
                'total':purchase.product_id.price * purchase.purchase_num,
            }
            purchase_list.append(tmp_dict)
    templete = loader.get_template('scanner/index.html')
    context = {
        'history_id':history_id,
        'product_list':product_list,
        'purchase_list':purchase_list,
    }
    return HttpResponse(templete.render(context, request))