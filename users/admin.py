from django.contrib import admin
from .models import UserProfile,Plan,ExamTemplate
# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username','idcard','level','major','role','is_checked','create_time')#在管理界面显示的字段，即具体的属性与方法
    # list_filter = ['username','idcard']
    # search_fields = ['username','idcard']

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('plan_name','single_choice_num','single_choice_score','mul_choice_num','mul_choice_score','judge_num','judge_score','get_total_score')#在管理界面显示的字段，即具体的属性与方法


@admin.register(ExamTemplate)
class ExamTemplateAdmin(admin.ModelAdmin):
    list_display = ('exam_template_name', 'exam_name')  # 在管理界面显示的字段，即具体的属性与方法
