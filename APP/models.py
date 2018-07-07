import hashlib
from datetime import datetime

from django.contrib.auth.hashers import make_password, check_password
from django.db import models


class Main(models.Model):
    img = models.CharField(max_length=200)
    name = models.CharField(max_length=64)
    track_id = models.IntegerField(default=0)

    class Meta:
        abstract = True


class MainWheel(Main):
    class Meta:
        db_table = "axf_wheel"

    def __str__(self):
        return self.name


class MainNav(Main):
    class Meta:
        db_table = 'axf_nav'

    def __str__(self):
        return self.name


class MainMustBuy(Main):
    class Meta:
        db_table = 'axf_mustbuy'

    def __str__(self):
        return self.name


class MainShop(Main):
    class Meta:
        db_table = 'axf_shop'

    def __str__(self):
        return self.name


class MainShow(Main):
    categoryid = models.IntegerField(default=0)
    brandname = models.CharField(max_length=64)

    img1 = models.CharField(max_length=200)
    childcid1 = models.IntegerField(default=0)
    productid1 = models.IntegerField(default=0)
    longname1 = models.CharField(max_length=200)
    price1 = models.FloatField(default=0)
    marketprice1 = models.FloatField(default=0)

    img2 = models.CharField(max_length=200)
    childcid2 = models.IntegerField(default=0)
    productid2 = models.IntegerField(default=0)
    longname2 = models.CharField(max_length=200)
    price2 = models.FloatField(default=0)
    marketprice2 = models.FloatField(default=0)

    img3 = models.CharField(max_length=200)
    childcid3 = models.IntegerField(default=0)
    productid3 = models.IntegerField(default=0)
    longname3 = models.CharField(max_length=200)
    price3 = models.FloatField(default=0)
    marketprice3 = models.FloatField(default=0)

    class Meta:
        db_table = 'axf_mainshow'


class FoodTypes(models.Model):
    typeid = models.IntegerField(default=0)
    typename = models.CharField(max_length=16)
    childtypenames = models.CharField(max_length=200)
    typesort = models.IntegerField(default=0)

    class Meta:
        db_table = 'axf_foodtypes'


class Goods(models.Model):
    productid = models.IntegerField(default=0)
    productimg = models.CharField(max_length=200)
    productname = models.CharField(max_length=100)
    productlongname = models.CharField(max_length=200)
    isxf = models.BooleanField(default=False)
    pmdesc = models.CharField(max_length=200)
    specifics = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    marketprice = models.FloatField(default=0)
    categoryid = models.IntegerField(default=0)
    childcid = models.IntegerField(default=0)
    childcidname = models.CharField(max_length=100)
    dealerid = models.IntegerField(default=0)
    storenums = models.IntegerField(default=0)
    productnum = models.IntegerField(default=0)

    class Meta:
        db_table = 'axf_goods'


class UserInfo(models.Model):
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=64, unique=True)
    icon = models.ImageField(upload_to='icons', verbose_name='头像')
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'axf_user'

    def set_password(self, password):
        # md5 = hashlib.md5()
        # md5.update(password.encode('utf-8'))
        # password = md5.hexdigest()
        password = make_password(password)
        self.password = password

    def check_password(self, password):
        # md5 = hashlib.md5()
        # md5.update(password.encode('utf-8'))
        # password = md5.hexdigest()
        # return self.password == password
        return check_password(password, self.password)

    def __str__(self):
        return self.username


"""
使用property将方法转换成属性
    _password = models.CharField(max_length=256)

    @property
    def u_password(self):
        return self._password

    @u_password.setter
    def u_password(self, pwd):
        self._password = make_password(pwd)

    def check_password(self, pwd):

        return check_password(pwd, self._password)

"""


# 购物车
class Cart(models.Model):
    c_goods = models.ForeignKey(Goods)
    c_user = models.ForeignKey(UserInfo)
    c_is_select = models.BooleanField(default=True)
    c_goods_nums = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_cart'


# 订单
class Order(models.Model):
    o_uesr = models.ForeignKey(UserInfo)
    o_total_price = models.FloatField(default=0)
    """
    订单状态:
        0:下单未支付
        1:下单已支付
        2:下单未发货
        3:下单已发货
    """

    o_status = models.IntegerField(default=0)
    addtime = models.DateTimeField(datetime.now)

    class Meta:
        db_table = 'axf_order'


# 订单商品
class OrderGoods(models.Model):
    order = models.ForeignKey(Order)
    goods = models.ForeignKey(Goods)
    goods_num = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_ordergoods'
