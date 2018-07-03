from django.shortcuts import render, redirect
from django.urls import reverse

from .models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodTypes, Goods


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
    return redirect(reverse("axf:marketWithParams", kwargs={"typeid": "104749"}))


def marketWithParams(request, typeid):
    food_types = FoodTypes.objects.all()
    goods_list = Goods.objects.filter(categoryid=typeid)

    data = {
        "title": "闪购",
        'food_types': food_types,
        'good_list': goods_list,
        'typeid': int(typeid),
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
