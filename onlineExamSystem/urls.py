"""onlineExamSystem0 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('user/',include('users.urls')),
    path('admin/', admin.site.urls),
    path('',views.HomeView.as_view(),name='home'),
    path('personal_info/', views.PersonalInfo.as_view(), name='personal_info'),

    path('student_index/',views.StudentIndexView.as_view(),name='student_index'),
    path('check_grade/',views.StudentCheckGradeView.as_view(),name='check_grade'),


    path('examing/',views.ExamingView.as_view(),name='examing'),

    path('add_question/',views.AddQuestionView.as_view(),name='add_question'),
    path('knowledge_manage/',views.KnowledgeManageView.as_view(),name='knowledge_manage'),
    path('knowledge_query/',views.QueryKnowledgeView.as_view(),name='knowledge_query'),

    path('question_store/',views.QuestionStoreView.as_view(),name='question_store'),
    path('question_query/',views.QueryQuestionView.as_view(),name='question_query'),

    path('admin_index/',views.AdminIndexView.as_view(),name='admin_index'),
    path('query_user/',views.AdminQueryUserView.as_view(),name='query_user'),
    path('add_user/',views.AdminAddUserView.as_view(),name='add_user'),

    path('plan_manage/',views.AdminPlanManageView.as_view(),name='plan_manage'),
    path('change_plan/',views.AdminChangePlanView.as_view(),name='change_plan'),
    path('query_plan/',views.AdminQueryPlanView.as_view(),name='query_plan'),

    path('exam_template/',views.AdminExamTemplateView.as_view(),name='exam_template'),
    path('change_exam_template/',views.AdminChangeExamTemplateView.as_view(),name='change_exam_template'),
    path('query_exam_template/', views.AdminQueryExamTemplateView.as_view(), name='query_exam_template'),

    path('exam_create/',views.AdminExamCreateView.as_view(),name='exam_create'),
    path('change_exam/',views.AdminChangeExamView.as_view(),name='change_exam'),
    path('query_exam/', views.AdminQueryExamView.as_view(), name='query_exam'),

    path('exam_allot/',views.ExamAllotView.as_view(),name='exam_allot'),
    path('query_exam_allot/',views.QueryExamAllotView.as_view(),name='query_exam_allot'),
    path('export_grade/',views.ExportView.as_view(),name='export_grade'),

    path('exam_record/',views.ExamRecordView.as_view(),name='exam_record'),
    path('query_exam_record/',views.QueryExamRecordView.as_view(),name='query_exam_record'),

    path('exam_grade/',views.ExamGradeView.as_view(),name='exam_grade'),
    path('query_exam_grade/',views.QueryExamGradeView.as_view(),name='query_exam_grade'),


    # path('ex/',views.export_excel,name='ex'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)