# -*- coding: utf-8 -*- 
__author__ = 'yank'
__date__ = '2018/7/3/12:18'

from django.conf.urls import url

from APP import views

urlpatterns = [
    url(r'^home/', views.home, name='home'),
    url(r'^market/', views.market, name='market'),
    url(r'^marketwithparams/(?P<typeid>\d+)/', views.marketWithParams, name='marketWithParams'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^mine/', views.mine, name='mine'),
]
