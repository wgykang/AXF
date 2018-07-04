from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodTypes, Goods

ALL_TYPE = '0'

TOTAL_RULE = '0'

PRICE_UP = '1'

PRICE_DOWN = '2'

def home(request):
    wheels = MainWheel.objects.all()
    navs = MainNav.objects.all()
    mustbuys = MainMustBuy.objects.all()
    shops = MainShop.objects.all()
    shop1 = shops[0:1]
    shop1_3 = shops[1:3]
    shop3_7 = shops[3:7]
    shop7_11 = shops[7:11]
    mainshows = MainShow.objects.all()

    data = {
        "title": "首页",
        "wheels": wheels,
        'navs': navs,
        'mustbuys': mustbuys,
        'shop1': shop1,
        'shop1_3': shop1_3,
        'shop3_7': shop3_7,
        'shop7_11': shop7_11,
        'mainshows': mainshows,
    }

    return render(request, 'home/home.html', context=data)


def market(request):
    return redirect(reverse("axf:marketWithParams", kwargs={"typeid": "104749", 'cid': '0', 'sort_rule': '0'}))


def marketWithParams(request, typeid, cid, sort_rule):
    food_types = FoodTypes.objects.all()

    if ALL_TYPE == cid:
        goods_list = Goods.objects.filter(categoryid=typeid)
    else:
        goods_list = Goods.objects.filter(categoryid=typeid).filter(childcid=cid)

    """
    全部分类:0#进口水果:110#国产水果:120
    数字ID是分类的标识
    切割#号
        [全部分类:0, 进口水果:110, 国产水果:120]
    切割:号
        [[全部分类,0], [进口水果,110], [国产水果,120]]
    """

    food_type = FoodTypes.objects.get(typeid=typeid)
    child_type_names = food_type.childtypenames
    child_type_names_list = child_type_names.split("#")
    child_type_name_list = []
    for child_type_name in child_type_names_list:
        child_type_name_list.append(child_type_name.split(':'))

    """
    综合排序:
            就是对筛选结果进行一个order_by
            
    服务器能接受对应的字段(排序字段)
    客户端发送排序字段:
            0: 综合排序
            1: 价格升序
            ...
    """
    if sort_rule == TOTAL_RULE:
        pass
    elif sort_rule == PRICE_UP:
        goods_list = goods_list.order_by('price')
    elif sort_rule == PRICE_DOWN:
        goods_list = goods_list.order_by('-price')

    data = {
        "title": "闪购",
        'food_types': food_types,
        'good_list': goods_list,
        'typeid': int(typeid),
        'child_type_name_list': child_type_name_list,
        'cid': cid,
        'sort_rule': sort_rule,
    }

    return render(request, 'market/market.html', context=data)


def cart(request):
    data = {
        "title": "购物车"
    }

    return render(request, 'cart/cart.html', context=data)


def mine(request):
    data = {
        "title": "我的"
    }

    return render(request, 'mine/mine.html', context=data)


def add_to_cart(request):
    print(request.GET)
    return JsonResponse({"msg": "ok"})