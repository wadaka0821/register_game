from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.utils import timezone
import uuid

from .models import Product, Purchase, History

# Create your views here.
def purchase(request, history_id):
    return HttpResponse("This is Purchase Page")

def count_up(request):
    print(request.POST.get('history_id'))
    print(request.POST.get('product_id'))

    history_id = uuid.UUID(request.POST.get('history_id'))
    product_id = uuid.UUID(request.POST.get('product_id'))
    history = History.objects.get(history_id=history_id)
    product = Product.objects.get(product_id=product_id)

    purchases = history.purchase_set.all()
    if len(purchases) and len(purchases.filter(product_id=product)):
        purchase = purchases.get(product_id=product)
        # purchase = purchases.get(product_id=product.product_id)
        purchase.purchase_num += 1
    else:
        purchase = history.purchase_set.create(product_id=product, purchase_num=1)
    history.total_price += purchase.product_id.price
    history.total_product += 1

    return HttpResponse('test')

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