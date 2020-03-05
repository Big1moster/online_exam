from django.apps import AppConfig

#django在创建app后会 在该app下生成apps.py  就是用于配置app显示名称的

class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = '用户信息'
    # 在init.py 下加上一个变量引用，因为django新建app时并没有把init文件加上引用
