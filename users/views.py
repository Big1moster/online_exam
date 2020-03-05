from django.contrib import auth
from django.urls import reverse
from django.shortcuts import render,redirect
from django.views.generic.base import View  # 基于类的view

from .models import UserProfile
from .forms import RegForm,LoginForm

class LogoutView(View):
    def get(self,request):
        auth.logout(request)
        return redirect(reverse('home'))

class LoginView(View):
    def get(self,request): # 当是get请求时自动调用该方法
        login_form = LoginForm()
        #如果用户此时不在登录状态
        if not request.user.is_authenticated:
            try:
                #检查cookie是否记住该用户
                username = request.get_signed_cookie('username',salt='i am salt')   # 解密cookie, salt是盐值
                password = request.get_signed_cookie('password',salt='i am salt')
                user = auth.authenticate(username=username,password=password)
                #如果记住了，则将用户名和密码填好
                if user is not None:
                    login_form.fields['password'].widget.attrs['value'] = password
                    login_form.fields['username'].widget.attrs['value'] = username   #设置表单初始值
            except:
                pass
        return render(request,'login.html',{'login_form':login_form})
    def post(self,request):
        login_form = LoginForm(request.POST)  # login_form.errors 实际上是个dict  login_form.errors.username 如果存在则说明username字段出错
        if login_form.is_valid():  # 该方法会判断字段是否符合我们定义
            user = login_form.cleaned_data['user']
            if user.role == 'student':
                response = redirect(request.GET.get('from', reverse('home')))
            elif user.role == 'administrator':
                response = redirect(reverse('admin_index'))
            else:
                response = redirect(reverse('teacher'))
            if request.POST.get('is_remember',False) == 'remember':
                response.set_signed_cookie("username", login_form.cleaned_data['username'], max_age=60 * 60 * 12, salt='i am salt' )  #超时时间
                response.set_signed_cookie("password", login_form.cleaned_data['password'], max_age=60 * 60 * 12, salt='i am salt') #加密的cookie , salt是盐值
            auth.login(request, user)
            return response
        else:
            return render(request, 'login.html', {'login_form' : login_form})

class RegisterView(View):
    def get(self,request):
        reg_form = RegForm()
        context = {}
        context['reg_form'] = reg_form
        return render(request, 'register.html', context)
    def post(self,request):
        reg_form = RegForm(request.POST)
        # 数据是有效的即经过了验证
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            idcard = reg_form.cleaned_data['idcard']
            password = reg_form.cleaned_data['password']
            level = reg_form.cleaned_data['level']
            major = reg_form.cleaned_data['major']
            role = reg_form.cleaned_data['role']
            # create方法不仅创建了新的对象，而且直接将信息存储到数据库里。
            user = UserProfile.objects.create_user(username=username, idcard=idcard, password=password,level=level,major=major,role=role)
            # 登录用户,必须要request参数
            auth.login(request, user)

            if user.role == 'student':
                return redirect(request.GET.get('from', reverse('home')))
            elif user.role == 'administrator':
                if user.is_checked:
                    return redirect(reverse('admin_index'))
                else:
                    auth.logout(request)
                    return render(request,'waiting_checked.html',{})
            else:
                return redirect(reverse('teacher'))
            # 跳转到点击注册的那个页面
        else:
            return render(request,'register.html',{'reg_form':reg_form})
