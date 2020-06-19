import datetime
import urllib

import kkb
import requests
import xml.etree.ElementTree as ET
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from kkb import get_context



from .models import Orders, Products, PayForm



def payments_view(request):
    if request.method == 'POST':
        form = PayForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/failure/')
    else:
        form = PayForm()
    return render(request, 'pay.html', {'form': form})

def pay_confirm(request):
    data = request.POST #принимаем данные: user_id, product, name_bank
    user = request.user
    product = Products.objects.first()
    orders_last = Orders.objects.last()
    if orders_last:
        new_orders_id = orders_last.order_id + 1
    else:
        new_orders_id = 2000001
    orders = Orders.objects.create(users=user,
                                   name_bank='kkb',
                                   product=product,
                                   order_id=new_orders_id)
    email = user.email
    backlink = 'http://127.0.0.1:8000/view/payments/'
    postlink = 'http://127.0.0.1:8000/view/result/'
    failurebacklink = 'http://127.0.0.1:8000/view/failure/'
    context = kkb.get_context(order_id=orders.order_id, amount=orders.product.amount, currency_id="398")

    data_bank = {'Signed_Order_B64': context,
                 'email': email,
                 'BackLink': backlink,
                 'PostLink': postlink,
                 'FailureBackLink': failurebacklink}

    return render(request, 'confirmation.html', {'data': data, 'data_bank': data_bank})


def pay_result(request):
    response = request.POST['response']
    print(response)
    #делаем проверку подписи банка
    result = kkb.postlink(response)
    print(result.status)
    if result.status:
        order = Orders.objects.filter(order_id=result.data['ORDER_ID'])
        print(order)
        # сделать проверку  and result.data['DEPARTMENT_MERCHANT_ID'] == settings.MERCHANT_ID
        # проверка суммы
        if result.data['ORDER_AMOUNT'] == order.product.amount:
            print(result.data['ORDER_ID'])
            Orders.objects.filter(order_id=result.data['ORDER_ID']).update(
                                           bank_response=True,
                                           time_transaction=result.data['ORDER_ID'],
                                           detail_response=result.data['PAYMENT_RESPONSE_CODE'])
        else:
            Orders.objects.filter(order_id=result.data['ORDER_ID']).update(
                bank_response=False,
                time_transaction=result.data['ORDER_ID'],
                response_code= 'No correct amount or merchant_id')
    else:
        print(result.message)
    return HttpResponse('result')


def payments_complete(request):
    # data = request.POST
    # order = Orders.objects.filter(order_id=data.order_id)
    # if order.bank_response == True:
    #     xml = get_context(order_id=order.order_id, amount=order.product.amount, b64=False)
    #
    #     url = 'https://testpay.kkb.kz/jsp/remote/checkOrdern.jsp?'+ url_code
    #     url_code = urllib.parse.quote_plus(xml_response)

    return HttpResponse('success')


def pay_failure(request):
    # order_last = Orders.objects.last()
    # print(order_last.order_id)
    #
    # xml = get_context(order_id=order_last.order_id, amount=order_last.product.amount,b64=False)
    # print(xml)
    #
    # xml_response = '<xml><document><merchant id= "92061103">< order id = "'+ str(order_last.order_id) +'"/></merchant>' + xml + '<merchant_sign type="RSA" cert_id="00c183d70b">VoyZnN8sj0RvfgJj4ZesBM7F+2HH6KMEmNeAerhl8vr8vsfPWBBPpfukh/X7oKCo2wvmmKqIWmzrtZEt9poLPnfHWD9kkVwX/FW8puOSxZDmr2faWxssNP6YE/YlQmswrWxpzgsYRwQR45PTNIhyJNUssWHWIYzWRfcha7CchDI=</merchant_sign></document></xml>'
    # url_code = urllib.parse.quote_plus(xml_response)
    # url = 'https://testpay.kkb.kz/jsp/remote/checkOrdern.jsp?'+ url_code
    # print(url)
    # response = requests.get(url)
    # print(response.status_code)
    # print(response.content)

    return HttpResponse('failure')

