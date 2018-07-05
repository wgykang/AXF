#### Django发送邮件功能

- Django文档说明:https://docs.djangoproject.com/en/2.0/topics/email/

```python
from django.core.mail import send_mail

send_mail(
    'Subject here',      
    'Here is the message.',
    'from@example.com',
    ['to@example.com'],
    fail_silently=False,
)
```

- **send_mail参数说明:**
  - 第一个参数:邮件主题
  - 第二个参数:message
  - 第三个参数:发送者的邮箱地址
  - 第四个参数:接受者的邮箱地址
- 其他必要配置(setting.py配置),常量名不可变

```python
EMAIL_HOST = 'smtp.163.com'    # 指定的SMTP主机

EMAIL_PORT = 25				  # 主机端口

EMAIL_HOST_USER = "13971039366@163.com"    # 用户

EMAIL_HOST_PASSWORD = "admin123"		  # 密码
```

- 发送邮件的逻辑

```python
from django.core.mail import send_mail
from django.template import loader

def send_mail_to(username, active_url, receive_mail):
    subject = "欢迎加入×××"

    # 添加到缓存中
    temp = loader.get_template('user/active.html')

    data = {
        "username": username,
        "active_url": active_url
    }

    # 渲染页面
    html_message = temp.render(context=data)

    send_mail(subject, "xxx", from_email="13971039366@163.com", recipient_list=[receive_mail],
              html_message=html_message)
```

- 用户注册时自动发送激活邮件

```python
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
```

- 登录时候验证逻辑

```python
class LoginView(View):
    def get(self, request):
        # 用于提示用户登录情况
        msg = request.session.get('login_msg')
		
        data = {}

        if msg:
            data['msg'] = msg
            # 再次刷新页面删除session,避免提示信息一直存在页面上
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
```

