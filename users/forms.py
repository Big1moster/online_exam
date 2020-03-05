from django import forms
from .models import UserProfile
from django.contrib import auth

# 在验证失败是抛出自定义错误信息，就必须使用forms.ValidationError('msg错误信息',code="")
# 实例化该类时必须传入一个dict参数一般是request.POST，然后他会将表单里的字段与Form里定义的字段进行匹配，匹配后再做验证
# 表单验证失败后根本不会去数据库中查询
class RegForm(forms.Form):
    username = forms.CharField(label="用户名"
                               ,max_length=20,
                               min_length=3,
                               widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入3-30位的用户名'}))

    idcard = forms.CharField(label='身份证号'
                             ,max_length=18,
                             min_length=18,
                             widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入18位的身份证号'}))

    password = forms.CharField(label="密码",
                               min_length=6,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

    ensure_password = forms.CharField(label="再输入密码",
                                     min_length=6,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '再次输入密码'}))

    level = forms.CharField(label='层次',widget=forms.Select(choices=(
        ('本科','本科'),
        ('专科','专科'),
    ),attrs={'class': 'form-control'}))

    major = forms.CharField(label='层次', widget=forms.Select(choices=(
        ('软件工程', '软件工程'),
        ('法学', '法学'),
        ('数学', '数学'),
    ), attrs={'class': 'form-control'}))

    role = forms.CharField(label='层次', widget=forms.Select(choices=(
        ('student', '学生'),
        ('teacher', '教师'),
        ('administrator', '管理员'),
    ), attrs={'class': 'form-control'}))

#加下划线 专门正对字段进行验证
    def clean_username(self):
        username = self.cleaned_data['username']
        if UserProfile.objects.filter(username = username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_idcard(self):
        idcard = self.cleaned_data['idcard']
        if UserProfile.objects.filter(idcard = idcard).exists():
            raise forms.ValidationError('该身份证已注册')
        return idcard

    def clean_ensure_password(self):
        password = self.cleaned_data['password']
        ensure_password = self.cleaned_data['ensure_password']
        if password != ensure_password:
            raise forms.ValidationError('密码不一致')
        return ensure_password



class LoginForm(forms.Form):
    #定制表单   required=True该字段必填，为空则报错 ，input里面的name必须和此处的字段名相同,不然不会做验证
    #min_length 当长度小于指定长度时，直接form验证失败，不会去数据库里面查，这样对数据库也是一种减负操作
    username = forms.CharField(max_length=20,
                               min_length=3,label="用户名",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入用户名'}))  #默认label就是字段名username，默认required=True，不需要时可以手动设置
    #widget设置input的type属性值为password  ,添加一些bootstrap的类，做样式
    password = forms.CharField(min_length=6,label="密码",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入密码'}))


    # 注意，你覆盖的Form.clean()引发的任何错误将不会与任何特定的字段关联。
    # 它们位于一个特定的“字段”（叫做__all__）中，如果需要可以通过 non_field_errors() 方法访问

    def clean(self):  #因为没有对具体字段进行clean_，所以具体字段不会有errors，只有login_form.errors才包含错误
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not UserProfile.objects.filter(username = username).exists():
            raise forms.ValidationError('用户名不存在')
        else:
            #用户验证可以不用request参数，login方法必须要
            user = auth.authenticate(username=username,password=password)
            if user is  None:
                raise forms.ValidationError('密码不正确')
            elif not user.is_checked:
                raise forms.ValidationError('该用户正在审核中')
            else:
                #将验证后的用户返回，到views中登录
                self.cleaned_data['user'] = user
        return self.cleaned_data