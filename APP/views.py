import uuid

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from APP.viewshelp import get_user, send_mail_to, get_user_id, get_total_price
from .models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodTypes, Goods, Cart
from .models import UserInfo

ALL_TYPE = '0'

TOTAL_RULE = '0'

PRICE_UP = '1'

PRICE_DOWN = '2'


# 首页
@cache_page(60)
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


# 闪购页面展示
@cache_page(60)
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


# 我的页面展示
def mine(request):
    user_id = request.session.get('user_id')
    data = {
        "title": "我的",
        'is_login': False,
    }
    if user_id:
        user = UserInfo.objects.get(pk=user_id)
        data['is_login'] = True
        data['username'] = user.username
        data['icon'] = '/static/upload/' + user.icon.url
    return render(request, 'mine/mine.html', context=data)


# 注册
class UserView(View):

    def get(self, request):
        return render(request, 'user/register.html')

    def post(self, request):
        username = request.POST.get('u_username')
        email = request.POST.get('u_email')
        password = request.POST.get('u_password')
        icon = request.FILES.get('u_icon')
        user = UserInfo()
        user.username = username
        user.email = email
        """
        后台密码加密
        """
        user.set_password(password)
        # user.password = password
        user.icon = icon
        user.save()
        # 生成一个token,通过uuid
        token = str(uuid.uuid4())
        # 设置缓存key为token,value为user.id
        cache.set(token, user.id, timeout=60 * 60 * 24)
        # 激活地址
        active_url = "http://localhost:8000/axf/active/?token=" + token
        # 发送激活邮件
        send_mail_to(username, active_url, email)
        # request.session['user_id'] = user.id
        # 重定向到登录页面
        response = redirect(reverse('axf:login'))
        return response


# 登出
def logout(request):
    # cookie和session一起清除
    request.session.flush()
    return redirect(reverse('axf:mine'))


"""
class UserLogin(TemplateView):
    # 和View中get类似
    template_name = 'user/login.html'

    def post(self, request):
        # 登录验证
        pass
"""


# 登录
class LoginView(View):
    def get(self, request):
        msg = request.session.get('login_msg')

        data = {}

        if msg:
            data['msg'] = msg
            del request.session['login_msg']
        return render(request, 'user/login.html', context=data)

    def post(self, request):
        username = request.POST.get('u_username')
        password = request.POST.get('u_password')
        user = get_user(username)
        if not user:
            request.session['login_msg'] = "用户未注册"
            return redirect(reverse('axf:login'))
        # 密码验证
        if user.check_password(password):
            if user.is_active:
                request.session['user_id'] = user.id
                response = redirect(reverse('axf:mine'))
                return response
            # 用户未激活的
            request.session['login_msg'] = "请先验证邮箱激活用户"
            return redirect(reverse("axf:login"))
        # 密码错误
        request.session['login_msg'] = "用户名或密码错误"
        return redirect(reverse('axf:login'))


# 判断用户名是否存在
def check_user(request):
    username = request.GET.get('username')
    user = get_user(username)
    data = {
        'msg': '<span style="color: green">用户名可用</span>'
    }

    if user:
        data['status'] = '901'
        data['msg'] = '<span style="color: red">用户名已存在</span>'
    else:
        data['status'] = '200'
    return JsonResponse(data)


# 激活用户
def active(request):
    # 获取token
    token = request.GET.get('token')
    # 缓存中获取user_id
    user_id = cache.get(token)

    if user_id:
        # token使用一次后删除,避免可以多次激活
        cache.delete(token)
        # 获取对应用户
        user = UserInfo.objects.get(pk=user_id)
        # 激活用户
        user.is_active = True
        # 保存
        user.save()

        return redirect(reverse('axf:login'))
    else:
        return HttpResponse("激活信息过期，请重新申请激活邮件")


# 添加购物车
def add_to_cart(request):
    user_id = request.session.get('user_id')
    user = get_user_id(user_id)
    data = {}
    if not user:
        # 重定向到用户登录
        data['status'] = '902'
        data['msg'] = '请先登录'
        return JsonResponse(data)
    else:
        goods_id = request.GET.get('goods_id')
        carts = Cart.objects.filter(c_user=user).filter(c_goods_id=goods_id)
        if carts.exists():
            cart = carts.first()
            cart.c_goods_nums = cart.c_goods_nums + 1
            cart.save()
        else:
            cart = Cart()
            cart.c_goods_id = goods_id
            cart.c_user_id = user_id
            cart.save()
        data['cart_num'] = cart.c_goods_nums
        data['msg'] = '添加成功'
        data['status'] = '201'
        return JsonResponse(data)


# 购物车页面
def cart(request):
    user_id = request.session.get('user_id')
    user = get_user_id(user_id)
    if not user:
        return redirect(reverse("axf:login"))
    # cart_set 外键对应的隐形属性， 本质上也是一个Manager对象
    carts = user.cart_set.all()
    # 进入购物车页面判断是否需要全选
    all_select = True
    if carts.filter(c_is_select=False).exists():
        all_select = False
    data = {
        "title": "购物车",
        "carts": carts,
        'total_price': get_total_price(user_id),
        'all_select': all_select
    }

    return render(request, 'cart/cart.html', context=data)


# 改变购物车选取的状态
# 判断登录状态,判断购物车数据是否存在
def change_cart_status(request):
    cart_id = request.GET.get('cart_id')
    cart_obj = Cart.objects.get(pk=cart_id)
    cart_obj.c_is_select = not cart_obj.c_is_select
    cart_obj.save()

    all_select = True

    if cart_obj.c_is_select:
        user_id = request.session.get("user_id")
        carts = Cart.objects.filter(c_user_id=user_id).filter(c_is_select=False)
        if carts.exists():
            all_select = False

    data = {
        'msg': 'success',
        'status': '200',
        'is_select': cart_obj.c_is_select,
        'all_select': all_select,
        'total_price': get_total_price(request.session.get('user_id'))
    }
    return JsonResponse(data)


def change_cart_list_status(request):
    action = request.GET.get('action')
    cart_list = request.GET.get('cart_list')
    carts = cart_list.split('#')
    if action == 'select':
        # 选出主键在已有列表的所有元素
        # Cart.objects.filter(pk__in=carts).update({'c_is_select': True})
        for cart_id in carts:
            cart_obj = Cart.objects.get(pk=cart_id)
            cart_obj.c_is_select = True
            cart_obj.save()
    elif action == 'unselect':
        for cart_id in carts:
            cart_obj = Cart.objects.get(pk=cart_id)
            cart_obj.c_is_select = False
            cart_obj.save()
    data = {
        'msg': 'success',
        'status': '200',
        'action': action,
        'total_price': get_total_price(request.session.get('user_id'))
    }
    return JsonResponse(data)


# 购物车数量减少
def sub_to_cart(request):
    cart_id = request.GET.get('cart_id')
    cart_obj = Cart.objects.get(pk=cart_id)
    data = {
        'msg': 'success',
        'status': '200',
    }
    if cart_obj.c_goods_nums == 1:
        cart_obj.delete()
        data["goods_num"] = 0
    else:
        cart_obj.c_goods_nums = cart_obj.c_goods_nums - 1
        cart_obj.save()
        data["goods_num"] = cart_obj.c_goods_nums
    data['total_price'] = get_total_price(request.session.get('user_id'))
    return JsonResponse(data)
