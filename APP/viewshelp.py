# -*- coding: utf-8 -*-
__author__ = 'yank'
__date__ = '2018/7/5/10:02'

from django.db.models import Q
from django.template import loader
from django.core.mail import send_mail

from .models import UserInfo, Cart


def get_user(username):
    try:
        user = UserInfo.objects.get(username=username)
        return user
    except:
        return None


def send_mail_to(username, active_url, receive_mail):
    subject = "欢迎加入×××"

    # 添加到缓存中
    temp = loader.get_template('user/active.html')

    data = {
        "username": username,
        "active_url": active_url
    }

    # 渲染
    html_message = temp.render(context=data)

    send_mail(subject, "xxx", from_email="13971039366@163.com", recipient_list=[receive_mail],
              html_message=html_message)


def get_user_id(user_id):
    try:
        user = UserInfo.objects.get(pk=user_id)
        return user
    except:
        return None


def get_total_price(user_id):
    carts = Cart.objects.filter(c_user_id=user_id)
    total_price = 0
    for cart in carts:
        if cart.c_is_select:
            total_price += cart.c_goods_nums * cart.c_goods.price
    return total_price
