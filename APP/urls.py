# -*- coding: utf-8 -*- 
__author__ = 'yank'
__date__ = '2018/7/3/12:18'

from django.conf.urls import url

from APP import views
from APP.views import UserView, LoginView

urlpatterns = [
    url(r'^home/', views.home, name='home'),
    url(r'^market/', views.market, name='market'),
    url(r'^marketwithparams/(?P<typeid>\d+)/(?P<cid>\d+)/(?P<sort_rule>\d+)/', views.marketWithParams,
        name='marketWithParams'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^mine/', views.mine, name='mine'),
    url(r'^addtocart/', views.add_to_cart, name='add_to_cart'),
    url(r'^user/', UserView.as_view(), name='user'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^checkuser/', views.check_user, name='checkuser'),
    url(r'^active/', views.active, name='active'),
    url(r'^changecartstatus/', views.change_cart_status, name='change_cart_status'),
    url(r'^changecartliststatus/', views.change_cart_list_status, name='change_cart_list_status'),
    url(r'^sub/', views.sub_to_cart, name='sub_to_cart'),
]
