from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.http import JsonResponse
from django.views.generic.base import View
from django.urls import reverse
from users.models import UserProfile,Plan,ExamTemplate,Exam,Question,Knowledge,ExamRecord
from django import forms
from .forms import EditorUserForm,AddUserForm,AddExamTemplateForm,EditorPlanForm,AddPlanForm,EditorExamTemplateForm,ChangeUserInfoForm,QuestionInfoForm,EditorQuestionForm
from django.core.paginator import Paginator
from . import settings
from datetime import datetime
import json
import random
import xlwt
from io import BytesIO
from django.contrib.auth.hashers import make_password

class HomeView(View):
    def get(self,request):
        return render(request, 'home.html', {})

class StudentCheckGradeView(View):
    def get(self,request):
        content = {}
        query_form = request.session.get('query_grade_form', {})
        if query_form:
            content.update(request.session.get('query_grade_form', {}))
            del request.session['query_grade_form']
            exam_records = ExamRecord.objects.all()
            if query_form['subject'] !="all":
                exam_records = ExamRecord.objects.filter(exam__exam_template__subject=query_form['subject'])
            if query_form['exam_th'] != "all":
                exam_records = exam_records.filter(exam__exam_template__exam_th=query_form['exam_th'])
        else:
            exam_records = ExamRecord.objects.all()
        if exam_records.count():
            content['query_empty_error'] = f'该查询 {query_form}  ：结果为空'
        content = get_model_list_data(request, exam_records)
        content['all_subjects'] = ('英语', '语文', '生物', '化学')
        content['all_exam_ths'] = []
        content['last_query_form'] = query_form
        for exam_record in exam_records:
            content['all_exam_ths'].append(exam_record.exam.exam_template.exam_th)


        return render(request, 'check_grade.html', content)
    def post(self,request):
        query = {}
        query['subject'] = request.POST.get('subject', '')
        query['exam_th'] = request.POST.get('exam_th', '')
        request.session['query_grade_form'] = query
        return redirect(reverse('check_grade'))


class StudentIndexView(View):
    def get(self,request):
        if request.is_ajax():  #ajax 查询考试
            data = {}
            subject = request.GET.get('subject', '')
            exams = Exam.objects.filter(exam_template__subject=subject,allot__idcard=request.user.idcard)
            data['exams'] = []
            for exam in exams:
                dic = {}
                dic['pk'] = exam.pk
                dic['exam_name'] = exam.exam_name
                dic['major'] = exam.major
                dic['start_time'] = exam.exam_template.exam_start_time
                dic['end_time'] = exam.exam_template.exam_end_time
                data['exams'].append(dic)
            data['status'] = 'SUCCESS'
            data['exam_num'] = len(exams)
            return JsonResponse(data)
        content = {}
        content['all_subjects'] = ('英语', '语文', '生物', '化学')
        # if request.session.get('add_question_content',''):
        #     content.update(request.session.get('add_question_content'))
        #     del request.session['add_question_content']  #取到session后删除，否则后续会一直取到
        return render(request,'student_index.html',content)
    def post(self,request):
        if request.is_ajax():  #ajax 查询考试说明
            data = {}
            exam_id = request.POST.get('exam_id', '')
            exam = Exam.objects.filter(pk=exam_id).first()
            data['exam_describe'] = exam.exam_describe
            data['exam_subject'] = exam.exam_template.subject
            data['exam_start_time'] = exam.exam_template.exam_start_time
            data['exam_id'] = exam.id
            data['status'] = 'SUCCESS'
            return JsonResponse(data)


class ExamingView(View):
    def get(self,request):
        content = {}
        exam_id = request.GET.get('exam_id', '')
        user_id = request.GET.get('user_id', '')
        exam = Exam.objects.filter(pk=exam_id).first()  #正在考的试卷
        dic = json.loads(exam.question_id_ls)  # 教学：：只有dumps后的字符串才能进行loads，否则报错，直接将dict str的字符串也会报错


        all_questions = {'single_choice_objs': [], 'mul_choice_objs': [], 'judge_objs': []}
        for pk in dic['single_choice_id_ls']:
            all_questions['single_choice_objs'].append(Question.objects.filter(pk=pk).first())
        for pk in dic['mul_choice_id_ls']:
            all_questions['mul_choice_objs'].append(Question.objects.filter(pk=pk).first())
        for pk in dic['judge_id_ls']:
            all_questions['judge_objs'].append(Question.objects.filter(pk=pk).first())

        content.update(all_questions)
        content['exam'] = exam
        content['single_choice_num'] = len(all_questions['single_choice_objs'])
        content['mul_choice_num'] = len(all_questions['mul_choice_objs'])
        content['judge_num'] = len(all_questions['judge_objs'])
        content['question_num'] = len(all_questions['single_choice_objs'])+len(all_questions['mul_choice_objs'])+len(all_questions['judge_objs'])
        return render(request, 'examing.html', content)
    def post(self,request):
        if request.is_ajax():

            examed_score = 0
            exam_id = request.POST.get('exam_id','')
            exam = Exam.objects.filter(pk=exam_id).first()

            right_answer = []
            user_answer = []
            for k,v in request.POST.items():
                print(k)
                if k.count('answer'):
                    question_id = k.split('_')[-1]

                    question = Question.objects.filter(pk=question_id).first()
                    right_answer.append((k,question.answer))
                    user_answer.append((question_id,v))
                    if question.answer.lower().strip() == v.lower().strip():  #当答案正确时
                        if question.question_type == "单选题":
                            score = exam.exam_template.plan.single_choice_score
                        elif question.question_type == "多选题":
                            score = exam.exam_template.plan.mul_choice_score
                        else:
                            score = exam.exam_template.plan.judge_score

                        question.score = score
                        question.save()
                        examed_score += score
            ExamRecord.objects.create(exam_id=exam_id,user_id=request.user.id,answer=str(user_answer),grade=examed_score)
            data = {}
            data['examed_score'] = examed_score
            data['status'] = 'SUCCESS'
            data['right_answer'] = right_answer
            return JsonResponse(data)
        return render(request, 'examing.html', {})

class QuestionStoreView(View):  #题库管理
    def get(self,request):  #题库列表
        if request.is_ajax():  #删除
            question_id = request.GET.get('obj_unique', '')
            question = Question.objects.filter(pk=question_id).first()
            if question:
                question.delete()
                return SuccessResponse()
            else:
                return ErrorResponse('该知识点不存在')
        content = {}
        content['all_subjects'] = ('英语', '语文', '生物', '化学')
        content['all_knowledges'] = Knowledge.objects.all()
        content['all_difficults'] = ('简单', '一般', '困难', '极难')

        if request.session.get('add_question_store_content',''):
            content.update(request.session.get('add_question_store_content'))
            del request.session['add_question_store_content']  #取到session后删除，否则后续会一直取到
        if request.session.get('editoe_question_content',''):
            content.update(request.session.get('editoe_question_content'))
            del request.session['editoe_question_content']  #取到session后删除，否则后续会一直取到

        questions = Question.objects.all()
        content.update(get_model_list_data(request, questions))
        return render(request,'question_store.html',content)
    def post(self,request):  #批量导入,编辑
        content = {}
        file = request.FILES.get('question_store', None)
        if file:
            with file as f:
                questions_str = f.read().decode('utf8')  # 读取的是bytes类型，解码为中文字符串
                questions_str = questions_str.replace('\r\n','').replace('\'','')
                questions_ls = json.loads(questions_str) #将字符串转为pytoon数据类型
                error_add_ls = []
                for question in questions_ls:  # 遍历每个问题字典
                    question_form =  QuestionInfoForm(question)
                    if question_form.is_valid():
                        try:
                            knowledge_name = question['knowledge_name']

                            question_name = question['question_name']
                            if Question.objects.filter(question_name=question_name).exists():
                                raise forms.ValidationError('该问题已存在')


                            subject = question['subject']
                            level = question['level']
                            major = question['major']
                            knowledge,iscreate = Knowledge.objects.get_or_create(knowledge_name=knowledge_name,
                                                                                  subject=subject,
                                                                                  level=level,
                                                                                  major=major)

                            dic = {'question_name': question_name,
                                   'option': question['option'],
                                   'answer': question['answer'],
                                   'score': int(question['score']),
                                   'subject': subject,
                                   'question_type': question['question_type'],
                                   'difficult': question['difficult'],
                                   'knowledge': knowledge}

                            question = Question.objects.create(**dic)
                        except Exception as e:
                            error_add_ls.append(str(e))
                    else:
                        error = question_form.errors
                        error_add_ls.append(error)
                content['error_add_ls'] = error_add_ls if error_add_ls else ''

                # UserProfile.objects.bulk_create(ls)  #批量添加
                store_name = f'media/{request.user.username}_{file.name}'
                with open(store_name, 'wb') as store:  # 将上传的文件保存下来
                    for chunk in file.chunks():
                        store.write(chunk)  # 此处必须写入bytes类型
            request.session['add_question_store_content'] = content
            return redirect(reverse('question_store'))
        question_form = EditorQuestionForm(request.POST)
        if question_form.is_valid():
            old_question_name = question_form.data['old_question_name']
            question = Question.objects.filter(question_name=old_question_name).first()

            question.question_name = question_form.data['questionName']
            question.answer = question_form.cleaned_data['answer']
            question.score = int(question_form.cleaned_data['score'])
            question.question_type = question_form.cleaned_data['question_type']
            question.subject = question_form.cleaned_data['subject']
            question.difficult = question_form.cleaned_data['difficult']

            knowledge_name = question_form.cleaned_data['knowledge_name']
            konwledge = Knowledge.objects.filter(knowledge_name=knowledge_name).first()
            question.knowledge = konwledge

            question.save()
            content['success_change_msg'] = '修改成功'
        else:
            content['error_change_msg'] = '修改失败'
        request.session['editoe_question_content'] = content
        return redirect(reverse('question_store'))

class QueryQuestionView(View):  #查询方案
    def get(self,request):
        content = {}
        query_form = request.session.get('query_question_form','')
        knowledge_name = query_form['knowledge']
        knowledge = Knowledge.objects.filter(knowledge_name=knowledge_name).first()
        if query_form:
            del request.session['query_question_form']
            questions = Question.objects.filter(subject=query_form['subject'],difficult=query_form['difficult'],knowledge=knowledge).first()
            content.update(get_model_list_data(request, questions))
            if not questions.count():  #如果查询结果为空
                content['query_empty_error'] = f'该查询 {query_form}  ：结果为空'
            content['last_query_form'] = query_form
        return render(request, 'question_store.html', content)
    def post(self,request):
        query = {}
        query['subject'] = request.POST.get('subject','')
        query['knowledge'] = request.POST.get('knowledge', '')
        query['difficult'] = request.POST.get('difficult', '')
        request.session['query_question_form'] = query
        return redirect(reverse('question_query'))

class AddQuestionView(View):
    def get(self,request):
        content = {}
        content['all_subjects'] = ('英语', '语文', '生物', '化学')
        content['all_question_types'] = ('单选题', '多选题', '判断题')
        content['all_difficults'] = ('简单', '一般', '困难', '极难')
        content['all_knowledges'] = Knowledge.objects.all()
        if request.session.get('add_question_content',''):
            content.update(request.session.get('add_question_content'))
            del request.session['add_question_content']  #取到session后删除，否则后续会一直取到
        return render(request,'teacher_index.html',content)
    def post(self,request):
        content = {}
        subject = request.POST.get('subject','')
        question_type = request.POST.get('question_type', '')
        difficult = request.POST.get('difficult', '')
        knowledge = request.POST.get('knowledge', '')
        knowledge = Knowledge.objects.filter(knowledge_name=knowledge).first()

        question_name = request.POST.get('question_name', '')
        answer = request.POST.get('answer', '')
        score = request.POST.get('score', '')
        option_a = request.POST.get('option_a', '')
        option_b = request.POST.get('option_b', '')
        option_c = request.POST.get('option_c', '')
        option_d = request.POST.get('option_d', '')
        if question_type == "判断题":
            question = Question.objects.create(question_name=question_name,answer=answer,score=score,
                                    subject=subject,question_type=question_type,
                                    difficult=difficult,knowledge=knowledge)
        else:
            option = f"A、{option_a}\nB、{option_b}\nC、{option_c}\nD、{option_d}"
            question = Question.objects.create(question_name=question_name, answer=answer, score=score,option=option,
                                               subject=subject, question_type=question_type,
                                               difficult=difficult, knowledge=knowledge)
        content['success_create_msg'] = '创建成功'
        request.session['add_question_content'] = content
        return redirect(reverse('add_question'))

class KnowledgeManageView(View):
    def get(self,request):  #知识点列表
        if request.is_ajax():  #删除
            knowledge_id = request.GET.get('obj_unique', '')
            knowledge = Knowledge.objects.filter(pk=knowledge_id).first()
            if knowledge:
                knowledge.delete()
                return SuccessResponse()
            else:
                return ErrorResponse('该知识点不存在')

        content = {}
        content['all_levels'] = ('本科', '专科')
        content['all_majors'] = ('软件工程', '法学', '数学')
        content['all_subjects'] = ('英语', '语文', '生物', '化学')
        if request.session.get('add_knowledge_content',''):
            content.update(request.session.get('add_knowledge_content'))
            del request.session['add_knowledge_content']  #取到session后删除，否则后续会一直取到
        knowledges = Knowledge.objects.all()
        content.update(get_model_list_data(request, knowledges))
        return render(request,'knowledge_manage.html',content)
    def post(self,request):  #添加知识点
        content = {}
        knowledge_name = request.POST.get('knowledge_name','')
        if Knowledge.objects.filter(knowledge_name=knowledge_name).count():
            content['error_create_msg'] = '该知识点名重复'
        else:
            level = request.POST.get('level', '')
            major = request.POST.get('major', '')
            subject = request.POST.get('subject', '')
            knowledge = Knowledge.objects.create(knowledge_name=knowledge_name,level=level,major=major,subject=subject)
            content['success_create_msg'] = f'知识点：{knowledge_name} 创建成功'
        request.session['add_knowledge_content'] = content
        return redirect(reverse('knowledge_manage'))

class QueryKnowledgeView(View):  #查询试卷模板
    def get(self,request):
        content = {}
        content['all_levels'] = ('本科', '专科')
        content['all_subjects'] = ('英语', '语文', '生物', '化学')
        content['all_majors'] = ('软件工程', '法学', '数学')

        knowledges = Knowledge.objects.all()
        query_form = request.session.get('query_knowledge_form', '')
        query_knowledge = Knowledge.objects.filter(level=query_form.get('level',''),major=query_form.get('major',''),subject=query_form.get('subject',''))


        if not query_knowledge.count():  # 当返回 int 0时，返回empty_error 信息
            content['query_empty_error'] = f'该查询 {query_form}  ：结果为空'
        else:
            content.update(get_model_list_data(request, query_knowledge))

        content['last_query_form'] = query_form
        return render(request, 'knowledge_manage.html', content)
    def post(self,request):
        query = {}
        query['level'] = request.POST.get('level', '')
        query['major'] = request.POST.get('major', '')
        query['subject'] = request.POST.get('subject', '')
        request.session['query_knowledge_form'] = query
        return redirect(reverse('knowledge_query'))

class PersonalInfo(View):
    def get(self,request):
        content = {}
        if request.session.get('editor_user_content',''):
            content.update(request.session.get('editor_user_content',''))
            del request.session['editor_user_content']
        if request.user.role == "student":
            return render(request, 'student_personal_info.html', content)
        elif request.user.role == "teacher":
            return render(request, 'teacher_personal_info.html', content)
        else:
            return render(request, 'admin_personal_info.html', content)
    def post(self,request):
        content = {}
        #修改头像
        if request.FILES.get('user_touxiang',''):
            img = request.FILES.get('user_touxiang','')
            request.user.touxiang = img
            request.user.save()
            return redirect(reverse('personal_info'))
        #修改密码
        if request.is_ajax():
            old_pwd = request.POST.get('old_pwd','')
            new_pwd = request.POST.get('new_pwd', '')
            again_pwd = request.POST.get('new_pwd', '')
            if request.user.check_password(old_pwd): #如果旧密码检查正确
                error_msg = ''
                leng = len(new_pwd)
                if new_pwd!=again_pwd:
                    error_msg = '两次密码不匹配'

                elif len(new_pwd)>16 or len(new_pwd)<6:
                    error_msg = '密码长度必须大于5小于17'
                else:
                    # hash_pwd = make_password(new_pwd)
                    # request.user.password = hash_pwd #直接设置加密后的密码
                    request.user.set_password(new_pwd) #自动将明文加密
                    request.user.save()  #此时密码修改，当前用户直接退出了
                    return SuccessResponse()
                return ErrorResponse(error_msg)

        change_user_Form = ChangeUserInfoForm(request.POST)
        if change_user_Form.is_valid():
            old_username = request.POST.get('old_username','')
            user = UserProfile.objects.filter(username=old_username).first()
            user.username = change_user_Form.cleaned_data['username']
            user.idcard = request.POST.get('idcard','')
            user.save()
            content['success_change_msg'] = f'用户->{old_username}:修改成功'
        else:
            content['error_change_msg'] = change_user_Form.errors.get('idcard','') + change_user_Form.errors.get('username','')
        request.session['editor_user_content'] = content
        return redirect(reverse('personal_info'))
#分页数据 ,输入模型数据
def get_model_list_data(request,model_all_list):
    paginator = Paginator(model_all_list, settings.EACH_PAGE_USERS_NUM)  #创建分页器对象; 每5个进行分页
    page_num = request.GET.get('page', 1)  # 获取url的页面参数，默认为1
    page_of_objs = paginator.get_page(page_num)  #返回一个number页码 的Page对象， 不在范围则返回默认值1页码
    current_page_num = page_of_objs.number  # 获取当前页码,前后各两页
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + list(
        range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    content = {}
    content['objs'] = page_of_objs.object_list  #当前页的所有对象
    content['page_of_objs'] = page_of_objs
    content['page_range'] = page_range
    return content

#ajax请求成功 和失败 返回的响应信息
def SuccessResponse():
    data = {}
    data['status'] = 'SUCCESS'
    return JsonResponse(data)
def ErrorResponse(error_message):
    data = {}
    data['status'] = 'ERROR'
    data['ajax_delete_error_msg'] = error_message
    return JsonResponse(data)

class AdminIndexView(View):   #删除---展示---编辑用户
    def get(self,request):   #删除---展示用户
        if request.is_ajax():  #返回bool，如果是ajax请求，即删除
            idcard = request.GET.get('obj_unique', '')
            user = UserProfile.objects.filter(idcard=idcard).first()
            if user:
                user.delete()
                return SuccessResponse()
            else:
                return ErrorResponse('该用户不存在')

        users = UserProfile.objects.all()
        content = get_model_list_data(request, users)
        if request.session.get('editoe_user_content',''):
            content.update(request.session.get('editoe_user_content'))
            del request.session['editoe_user_content']  #取到session后删除，否则后续会一直取到

        return render(request, 'admin_index.html', content)
    def post(self,request):   #编辑用户
        if request.is_ajax():  #返回bool，如果是ajax请求，即更新审核状态
            idcard = request.POST.get('obj_unique', '')
            user = UserProfile.objects.filter(idcard=idcard).first()
            if user:
                user.is_checked = False if user.is_checked else True
                user.save()
                print(user.is_checked)
                return SuccessResponse()
            else:
                return ErrorResponse('该用户不存在')

        content = {}
        editor_user_form = EditorUserForm(request.POST)
        if editor_user_form.is_valid():
            old_username = editor_user_form.cleaned_data['old_username']
            user = UserProfile.objects.filter(username=old_username).first()
            if user.is_authenticated:
                user.username = editor_user_form.cleaned_data['username']
                user.idcard = editor_user_form.cleaned_data['idcard']
                user.level = editor_user_form.cleaned_data['level']
                user.major = editor_user_form.cleaned_data['major']
                user.role = editor_user_form.cleaned_data['role']
                user.save()
                content['success_change_msg'] = f'用户->{old_username}:修改成功'
        else:
            content['error_change_msg'] = editor_user_form.errors.get('idcard','') + editor_user_form.errors.get('username','')
        request.session['editoe_user_content'] = content
        return redirect(reverse('admin_index'))
class AdminQueryUserView(View): #查询用户
    def get(self,request):
        content = {}
        query_form = request.session.get('query_user_form',{})
        if query_form:
            del request.session['query_user_form']
            users = UserProfile.objects.filter(level=query_form.get('level',), major=query_form.get('major',''))
            if query_form.get('username',''):
                users = users.filter(username__icontains=query_form['username'])
            if query_form.get('idcard',''):
                users = users.filter(idcard__icontains=query_form['idcard'])
            content.update(get_model_list_data(request, users))
            if not users.count(): #当返回 int 0时，返回empty_error 信息
                content['query_empty_error'] = f'该查询 {query_form}  ：结果为空'
            content['last_query_form'] = query_form
        return render(request, 'admin_index.html', content)
    def post(self,request):
        query = {}
        query['level'] = request.POST.get('level','')
        query['major'] = request.POST.get('major', '')
        query['username'] = request.POST.get('username', '')
        query['idcard'] = request.POST.get('idcard', '')
        request.session['query_user_form'] = query
        return redirect(reverse('query_user'))

class AdminAddUserView(View):  # 添加用户
    def get(self,request):
        return render(request, 'add_user.html', {})

    def post(self,request):
        content = {}
        file = request.FILES.get('user_file',None)
        if file:
            with file as f:
                users_info = f.read().decode('gb2312')  #读取的是bytes类型，解码为中文字符串
                users_ls = users_info.split('\r\n')  #得到所有用户的列表
                error_add_ls = []
                for user_info in users_ls:  #遍历每个用户
                    if not user_info:
                        continue
                    fields = user_info.split(' ')    #单个用户各字段的信息
                    fields = [field for field in fields if field]   #得到干净的用户字段
                    try:
                        dic = {'username':fields[0],'password':fields[1],'idcard':fields[2],'level':fields[3],'major':fields[4],'role':fields[5]}
                        add_form = AddUserForm(dic)
                        if add_form.is_valid():
                            user = UserProfile.objects.create_user(**dict(add_form))
                    except Exception as e:
                        error_add_ls.append(str(e))
                content['error_add_ls'] = error_add_ls

                # UserProfile.objects.bulk_create(ls)  #批量添加
                store_name = f'media/{request.user.username}_{file.name}'
                with open(store_name,'wb') as store:   #将上传的文件保存下来
                    for chunk in  file.chunks():
                        store.write(chunk)  #此处必须写入bytes类型

        add_form = AddUserForm(request.POST)
        # 数据是有效的即经过了验证
        if add_form.is_valid():
            username = add_form.cleaned_data['username']
            idcard = add_form.cleaned_data['idcard']
            password = add_form.cleaned_data['password'][3:]
            level = add_form.cleaned_data['level']
            major = add_form.cleaned_data['major']
            role = add_form.cleaned_data['role']
            # create方法不仅创建了新的对象，而且直接将信息存储到数据库里。
            user = UserProfile.objects.create_user(username=username, idcard=idcard, password=password, level=level,
                                                   major=major, role=role)
            content['success_create_msg'] = f'用户：{username} 创建成功'
        else:
            content['idcard_error'] = add_form.errors.get('idcard','')
            content['username_error'] = add_form.errors.get('username','')
            content['last_post'] = request.POST

        return render(request, 'add_user.html', content)

class AdminPlanManageView(View): #方案管理
    def get(self,request): #方案列表
        plans = Plan.objects.all()
        content = get_model_list_data(request,plans)
        if request.session.get('add_plan_content',''):
            content.update(request.session.get('add_plan_content'))
            del request.session['add_plan_content']  #取到session后删除，否则后续会一直取到
        if request.session.get('editoe_plan_content',''):
            content.update(request.session.get('editoe_plan_content'))
            del request.session['editoe_plan_content']
        return render(request, 'plan_manage.html', content)
    def post(self,request):   #添加方案
        content = {}
        plan_form = AddPlanForm(request.POST)
        if plan_form.is_valid():
            plan_name = plan_form.cleaned_data['plan_name']
            single_choice_num = int(request.POST.get('single_choice_num','')) if request.POST.get('single_choice_num','') else 0   #如果没填则为o
            single_choice_score = int(request.POST.get('single_choice_score','')) if request.POST.get('single_choice_score','') else 0
            mul_choice_num = int(request.POST.get('mul_choice_num','')) if request.POST.get('mul_choice_num','') else 0
            mul_choice_score = int(request.POST.get('mul_choice_score','')) if request.POST.get('mul_choice_score','') else 0
            judge_num = int(request.POST.get('judge_num','')) if request.POST.get('judge_num','') else 0
            judge_score = int(request.POST.get('judge_score','')) if request.POST.get('judge_score','') else 0
            plan = Plan.objects.create(plan_name=plan_name,single_choice_num=single_choice_num,single_choice_score=single_choice_score,
                                mul_choice_num=mul_choice_num,mul_choice_score=mul_choice_score,
                                judge_num=judge_num,judge_score=judge_score
                                )
            content['success_create_msg'] = f'方案：{plan_name} 创建成功'
        else:
            content['error_create_msg'] = plan_form.errors.get('plan_name','')
        request.session['add_plan_content'] = content
        return redirect(reverse('plan_manage'))
class AdminQueryPlanView(View):  #查询方案
    def get(self,request):
        content = {}
        query_form = request.session.get('query_plan_form','')
        if query_form:
            del request.session['query_plan_form']
            plans = Plan.objects.filter(plan_name__icontains=query_form['plan_name'])
            content.update(get_model_list_data(request, plans))
            if not plans.count():  #如果查询结果为空
                content['query_empty_error'] = f'该查询 {query_form}  ：结果为空'
            content['last_query_form'] = query_form
        return render(request, 'plan_manage.html', content)
    def post(self,request):
        query = {}
        query['plan_name'] = request.POST.get('plan_name','')
        request.session['query_plan_form'] = query
        return redirect(reverse('query_plan'))
class AdminChangePlanView(View):
    def get(self,request):  #ajax删除方案
        plan_name = request.GET.get('obj_unique', '')
        plan = Plan.objects.filter(plan_name=plan_name).first()
        if plan:
            plan.delete()
            return SuccessResponse()
        else:
            return ErrorResponse('该用户不存在')
    def post(self,request):  #修改方案
        content = {}
        plan_form = EditorPlanForm(request.POST)

        if plan_form.is_valid():
            plan_name = plan_form.cleaned_data['plan_name']
            old_plan_name = plan_form.cleaned_data['old_plan_name']
            plan = Plan.objects.filter(plan_name=old_plan_name).first()
            single_choice_num = int(request.POST.get('single_choice_num', '')) if request.POST.get('single_choice_num','') else 0  # 如果没填则为o
            single_choice_score = int(request.POST.get('single_choice_score', '')) if request.POST.get(
                'single_choice_score', '') else 0
            mul_choice_num = int(request.POST.get('mul_choice_num', '')) if request.POST.get('mul_choice_num',
                                                                                             '') else 0
            mul_choice_score = int(request.POST.get('mul_choice_score', '')) if request.POST.get('mul_choice_score',
                                                                                                 '') else 0
            judge_num = int(request.POST.get('judge_num', '')) if request.POST.get('judge_num', '') else 0
            judge_score = int(request.POST.get('judge_score', '')) if request.POST.get('judge_score', '') else 0

            if plan:
                plan.plan_name = plan_name
                plan.single_choice_num = single_choice_num
                plan.single_choice_score = single_choice_score
                plan.mul_choice_num = mul_choice_num
                plan.mul_choice_score = mul_choice_score
                plan.judge_num = judge_num
                plan.judge_score = judge_score
                plan.save()
                content['success_change_msg'] = f'方案名->{plan_name}:修改成功'
        else:
            content['error_change_msg'] = plan_form.errors.get('plan_name', '')
        request.session['editoe_plan_content'] = content
        return redirect(reverse('plan_manage'))


class AdminExamTemplateView(View):  #试卷模板
    def get(self,request):
        content = {}
        content['all_plans'] = Plan.objects.all()
        content['all_subjects'] = ('英语','语文','生物','化学')
        content['all_difficults'] = ('简单','一般', '困难','极难')
        exam_templates = ExamTemplate.objects.all()
        content['all_exem_templates'] = exam_templates
        content.update(get_model_list_data(request, exam_templates))
        if request.session.get('editoe_exam_template_content',''):
            content.update(request.session.get('editoe_exam_template_content', {}))
            del request.session['editoe_exam_template_content']
        if request.session.get('add_exam_template_content',''):
            content.update(request.session.get('add_exam_template_content',{}))
            del request.session['add_exam_template_content']
        return render(request, 'exam_template.html', content)
    def post(self,request):   #添加试卷模板
        content = {}
        exam_template_form = AddExamTemplateForm(request.POST)
        if exam_template_form.is_valid():
            exam_template_name = exam_template_form.cleaned_data.get('exam_template_name','')
            exam_name = exam_template_form.cleaned_data.get('exam_name','')
            exam_th = int(request.POST.get('exam_th', '')) if request.POST.get('exam_th','') else 0
            subject = request.POST.get('subject', '')
            plan_name = request.POST.get('plan_name', '')
            plan = Plan.objects.filter(plan_name=plan_name).first()  #外键必须将外键对象加上去才能创建
            difficult = request.POST.get('difficult', '')
            exam_start_time = request.POST.get('exam_start_time', '')  #str 2019-01-01T08:23,该字段传入格式就是这样
            exam_end_time = request.POST.get('exam_end_time', '')
            exam_start_time = datetime.now().strptime(exam_start_time, "%Y-%m-%dT%H:%M")  #将时间字符串转换为时间格式
            exam_end_time = datetime.now().strptime(exam_end_time, "%Y-%m-%dT%H:%M")
            try:
                exam_template = ExamTemplate.objects.create(exam_template_name=exam_template_name,exam_name=exam_name,exam_th=exam_th,
                                                            subject=subject,plan=plan,difficult=difficult,
                                                            exam_start_time=exam_start_time,exam_end_time=exam_end_time)
                content['success_create_msg'] = f'试卷模板：{exam_template_name} 创建成功'
            except Exception as e:
                print(e)
        else:
            content['error_create_msg'] = exam_template_form.errors.get('exam_template_name', '') + exam_template_form.errors.get('exam_name', '')
        request.session['add_exam_template_content'] = content
        return redirect(reverse('exam_template'))
class AdminChangeExamTemplateView(View):
    def get(self,request):  #ajax删除试卷模板
        exam_template_name = request.GET.get('obj_unique', '')
        exam_template = ExamTemplate.objects.filter(exam_template_name=exam_template_name).first()
        if exam_template:
            exam_template.delete()
            return SuccessResponse()
        else:
            return ErrorResponse('该模板不存在')
    def post(self,request):  #修改试卷模板
        content = {}
        exam_template_form = EditorExamTemplateForm(request.POST)
        if exam_template_form.is_valid():
            old_exam_template_name = exam_template_form.cleaned_data['old_exam_template_name']
            exam_template_name = exam_template_form.cleaned_data['exam_template_name']
            old_exam_name = exam_template_form.cleaned_data['old_exam_name']
            exam_name = exam_template_form.cleaned_data['exam_name']
            exam_template = ExamTemplate.objects.filter(exam_template_name=old_exam_template_name).first()

            exam_template.exam_template_name = exam_template_name
            exam_template.exam_name = exam_name
            exam_template.exam_th = int(request.POST.get('exam_th', '')) if request.POST.get('exam_th', '') else 0
            exam_template.subject = request.POST.get('subject', '')
            plan_name = request.POST.get('plan_name', '')
            exam_template.plan = Plan.objects.filter(plan_name=plan_name).first()  # 外键必须将外键对象加上去才能创建
            exam_template.difficult = request.POST.get('difficult', '')
            exam_start_time = request.POST.get('exam_start_time', '')  # str 2019-01-01T08:23,该字段传入格式就是这样
            exam_end_time = request.POST.get('exam_end_time', '')
            exam_template.exam_start_time = datetime.now().strptime(exam_start_time, "%Y-%m-%dT%H:%M")  # 将时间字符串转换为时间格式
            exam_template.exam_end_time = datetime.now().strptime(exam_end_time, "%Y-%m-%dT%H:%M")
            exam_template.save()
            content['success_change_msg'] = f'试卷模板名->{exam_template_name}:修改成功'
        else:
            content['error_change_msg'] = exam_template_form.errors.get('exam_template_name', '') + exam_template_form.errors.get('exam_name', '')
        request.session['editoe_exam_template_content'] = content
        return redirect(reverse('exam_template'))
class AdminQueryExamTemplateView(View):  #查询试卷模板
    def get(self,request):
        content = {}
        content['all_plans'] = Plan.objects.all()
        content['all_subjects'] = ('英语', '语文', '生物', '化学')
        content['all_difficults'] = ('简单', '一般', '困难', '极难')
        exam_templates = ExamTemplate.objects.all()
        query_form = request.session.get('query_exam_template_form','')

        plan_name = query_form['plan_name']
        plan = get_object_or_404(Plan,plan_name=plan_name)
        exam_templates = ExamTemplate.objects.filter(subject=query_form['subject'],plan=plan, difficult=query_form['difficult'])
        if query_form['exam_template_name']:
            exam_templates = exam_templates.filter(exam_template_name=query_form['exam_template_name'])
        if query_form['exam_name']:
            exam_templates = exam_templates.filter(exam_name=query_form['exam_name'])
        if query_form['exam_th']:
            exam_templates = exam_templates.filter(exam_th=query_form['exam_th'])
        content.update(get_model_list_data(request, exam_templates))
        if not exam_templates.count():  # 当返回 int 0时，返回empty_error 信息
            content['query_empty_error'] = f'该查询 {query_form}  ：结果为空'
        content['last_query_form'] = query_form
        return render(request, 'exam_template.html', content)
    def post(self,request):
        query = {}
        query['exam_template_name'] = request.POST.get('exam_template_name', '')
        query['exam_name'] = request.POST.get('exam_name', '')
        query['exam_th'] = int(request.POST.get('exam_th', '')) if request.POST.get('exam_th', '') else 0
        query['subject'] = request.POST.get('subject', '')
        query['plan_name'] = request.POST.get('plan_name', '')
        query['difficult'] = request.POST.get('difficult', '')
        request.session['query_exam_template_form'] = query
        return redirect(reverse('query_exam_template'))

class AdminExamCreateView(View):
    def get(self,request):  #试卷列表
        content = {}
        content['all_levels'] = ('本科','专科')
        content['all_subjects'] = ('英语', '语文', '生物', '化学')
        content['all_majors'] = ('软件工程','法学','数学')
        content['all_templates'] = ExamTemplate.objects.all()
        exams = Exam.objects.all()
        content.update(get_model_list_data(request, exams))
        if request.session.get('random_add_exam_content',''):
            content.update(request.session.get('random_add_exam_content', {}))
            del request.session['random_add_exam_content']
        return render(request, 'exam_create.html', content)
    def post(self,request):    # 添加试卷模板
        content = {}
        exam_name = request.POST.get('exam_name', '')
        exam_template_name = request.POST.get('exam_template_name','')
        level = request.POST.get('level','')
        major = request.POST.get('major','')
        exam_num = int(request.POST.get('exam_num', '')) if request.POST.get('exam_num', '') else 0

        exam_obj_ls = []
        if exam_num>0:
            exam_template = ExamTemplate.objects.filter(exam_template_name=exam_template_name).first()
            subject = exam_template.subject
            difficult = exam_template.difficult
            single_choice_num = exam_template.plan.single_choice_num
            mul_choice_num = exam_template.plan.mul_choice_num
            judge_num = exam_template.plan.judge_num

            knowledges = Knowledge.objects.filter(level=level, major=major, subject=subject)
            question_objs = Question.objects.none()
            for knowledge in knowledges:
                questions = knowledge.question_set.all().filter(difficult=difficult) #从该知识点关联的所有题目中找到适合难度的题目
                question_objs = question_objs|questions     #对queryset进行合并
            single_choice_questions_qset = question_objs.filter(question_type='单选题')
            mul_choice_questions_qset = question_objs.filter(question_type='多选题')
            judge_questions_qset = question_objs.filter(question_type='判断题')

            for i in range(exam_num):
                single_choice_id_ls = []
                mul_choice_id_ls = []
                judge_id_ls = []
                for i in range(single_choice_num):
                    random_index = random.randint(0, len(single_choice_questions_qset) - 1)
                    single_choice_id_ls.append(single_choice_questions_qset[random_index].id)
                for i in range(mul_choice_num):
                    random_index = random.randint(0, len(mul_choice_questions_qset) - 1)
                    mul_choice_id_ls.append(mul_choice_questions_qset[random_index].id)
                for i in range(judge_num):
                    random_index = random.randint(0, len(judge_questions_qset) - 1)
                    judge_id_ls.append(judge_questions_qset[random_index].id)
                exam_dict = {'single_choice_id_ls': single_choice_id_ls, 'mul_choice_id_ls': mul_choice_id_ls,
                             'judge_id_ls': judge_id_ls}
                exam_dict = json.dumps(exam_dict)
                exam = Exam(exam_template=exam_template,major=major,level=level,exam_name=exam_name,question_id_ls = exam_dict)
                exam_obj_ls.append(exam)
            try:
                Exam.objects.bulk_create(exam_obj_ls)
                content['success_create_msg'] = f'成功随机生成{exam_num}张试卷'
            except Exception as e:
                print(e)
        else:
            content['error_create_msg'] = '随机生成失败'
        request.session['random_add_exam_content'] = content
        return redirect(reverse('exam_create'))
class AdminQueryExamView(View):  #查询试卷模板
    def get(self,request):
        content = {}
        content['all_levels'] = ('本科', '专科')
        content['all_subjects'] = ('英语', '语文', '生物', '化学')
        content['all_majors'] = ('软件工程', '法学', '数学')
        content['all_templates'] = ExamTemplate.objects.all()
        exams = Exam.objects.all()
        query_form = request.session.get('query_exam_form', '')
        exam_template = ExamTemplate.objects.filter(exam_template_name__icontains=query_form.get('exam_template','')).first()
        if exam_template:
            queried_exams_1 = exam_template.exam_set.all()
            queried_exams = queried_exams_1.filter(level__icontains=query_form.get('level',''),
                                                # subject__icontains=query_form.get('subject',''),
                                                major__icontains=query_form.get('major', '')
                                                )
            content.update(get_model_list_data(request, queried_exams))
            if not queried_exams.count():  # 当返回 int 0时，返回empty_error 信息
                content['query_empty_error'] = f'该查询 {query_form}  ：结果为空'
        else:
            content['query_empty_error'] = f'该查询 {query_form}  ：结果为空'
        content['last_query_form'] = query_form
        return render(request, 'exam_create.html', content)
    def post(self,request):
        query = {}
        query['level'] = request.POST.get('level', '')
        query['subject'] = request.POST.get('subject', '')
        query['major'] = request.POST.get('major', '')
        query['exam_template'] = request.POST.get('exam_template', '')
        request.session['query_exam_form'] = query
        return redirect(reverse('query_exam'))
class AdminChangeExamView(View):
    def get(self, request):  # 查询试卷
        exam_id = request.GET.get('obj_unique', '')
        exam = Exam.objects.filter(pk=exam_id).first()
        if exam:
            exam.delete()
            return SuccessResponse()
        else:
            return ErrorResponse('该试卷不存在')

    def post(self, request):
        content = {}
        exam_template_form = EditorExamTemplateForm(request.POST)
        if exam_template_form.is_valid():
            old_exam_template_name = exam_template_form.cleaned_data['old_exam_template_name']
            exam_template_name = exam_template_form.cleaned_data['exam_template_name']
            old_exam_name = exam_template_form.cleaned_data['old_exam_name']
            exam_name = exam_template_form.cleaned_data['exam_name']
            exam_template = ExamTemplate.objects.filter(exam_template_name=old_exam_template_name).first()

            exam_template.exam_template_name = exam_template_name
            exam_template.exam_name = exam_name
            exam_template.exam_th = int(request.POST.get('exam_th', '')) if request.POST.get('exam_th', '') else 0
            exam_template.subject = request.POST.get('subject', '')
            plan_name = request.POST.get('plan_name', '')
            exam_template.plan = Plan.objects.filter(plan_name=plan_name).first()  # 外键必须将外键对象加上去才能创建
            exam_template.difficult = request.POST.get('difficult', '')
            exam_start_time = request.POST.get('exam_start_time', '')  # str 2019-01-01T08:23,该字段传入格式就是这样
            exam_end_time = request.POST.get('exam_end_time', '')
            exam_template.exam_start_time = datetime.now().strptime(exam_start_time, "%Y-%m-%dT%H:%M")  # 将时间字符串转换为时间格式
            exam_template.exam_end_time = datetime.now().strptime(exam_end_time, "%Y-%m-%dT%H:%M")
            exam_template.save()
            content['success_change_msg'] = f'试卷模板名->{exam_template_name}:修改成功'
        else:
            content['error_change_msg'] = exam_template_form.errors.get('exam_template_name',
                                                                        '') + exam_template_form.errors.get('exam_name',
                                                                                                            '')
        request.session['editoe_exam_template_content'] = content
        return redirect(reverse('exam_template'))


class ExamAllotView(View):
    def get(self,request):  #试卷列表
        content = {}
        content['all_levels'] = ('本科','专科')
        content['all_subjects'] = ('英语', '语文', '生物', '化学')
        content['all_majors'] = ('软件工程','法学','数学')
        content['all_templates'] = ExamTemplate.objects.all()
        exams = Exam.objects.all()
        content.update(get_model_list_data(request, exams))
        return render(request, 'exam_allot.html', content)
    def post(self,request):    # ajax分配对象
        if request.is_ajax():
            data = {}
            exam_id = request.POST.get('exam_id', '')
            level = request.POST.get('level', '')
            major = request.POST.get('major', '')
            username = request.POST.get('username', '')
            idcard = request.POST.get('idcard', '')
            exam = Exam.objects.filter(pk=exam_id).first()
            users = UserProfile.objects.filter(level=level,major=major,username__icontains=username,idcard__icontains=idcard)

            data['users_ls'] = []
            for user in users:
                dic = {}
                dic['username'] = user.username
                dic['idcard'] = user.idcard
                dic['level'] = user.level
                dic['major'] = user.major
                dic['user_id'] = user.id
                data['users_ls'].append(dic)
            data['status'] = 'SUCCESS'
            data['user_num'] = len(users)
            return JsonResponse(data)

        else:
            user_id_ls = request.POST.getlist('item') #获取该多选框的所有选中的值组成的列表
            exam_id = request.POST.get('exam_id','')
            exam = Exam.objects.filter(pk=exam_id).first()
            print(dir(exam.allot))
            for pk in user_id_ls:
                user = UserProfile.objects.filter(pk=pk).first()

                exam.allot.add(user)
            exam.save()
            return redirect(reverse('exam_allot'))

class QueryExamAllotView(View):  #查询试卷模板
    def get(self,request):
        content = {}
        content['all_levels'] = ('本科', '专科')
        content['all_subjects'] = ('英语', '语文', '生物', '化学')
        content['all_majors'] = ('软件工程', '法学', '数学')
        content['all_templates'] = ExamTemplate.objects.all()
        query_form = request.session.get('query_exam_allot_form', {})
        exams = Exam.objects.filter(major=query_form.get('major', ''),level=query_form.get('level', ''))
        exam_objs = []
        for exam in exams:
            if exam.exam_template.subject.count(query_form.get('subject','')):
                if exam.exam_template.exam_template_name.count(query_form.get('exam_template','')):
                    exam_objs.append(exam)



        content.update(get_model_list_data(request, exam_objs))
        if not exam_objs:  # 当返回 int 0时，返回empty_error 信息
            content['query_empty_error'] = f'该查询 {query_form}  ：结果为空'
        content['last_query_form'] = query_form
        return render(request, 'exam_allot.html', content)
    def post(self,request):
        query = {}
        query['level'] = request.POST.get('level', '')
        query['subject'] = request.POST.get('subject', '')
        query['major'] = request.POST.get('major', '')
        query['exam_template'] = request.POST.get('exam_template', '')
        request.session['query_exam_allot_form'] = query
        return redirect(reverse('query_exam_allot'))


class ExamRecordView(View):
    def get(self,request):  #试卷列表
        if request.is_ajax():  #删除
            exam_record_id = request.GET.get('obj_unique', '')
            exam_record = ExamRecord.objects.filter(pk=exam_record_id).first()

            if exam_record:
                exam_record.delete()
                return SuccessResponse()
            else:
                return ErrorResponse('该考试记录不存在')
        content = {}
        content['all_levels'] = ('本科','专科')
        content['all_subjects'] = ('英语', '语文', '生物', '化学')
        content['all_majors'] = ('软件工程','法学','数学')
        exam_records = ExamRecord.objects.all()
        content.update(get_model_list_data(request, exam_records))
        if request.session.get('change_exam_record_content',''):
            content.update(request.session.get('change_exam_record_content', {}))
            del request.session['change_exam_record_content']
        return render(request, 'exam_record.html', content)
    def post(self,request):
        exam_record_id = request.POST.get('exam_record_id','')
        exam_record = ExamRecord.objects.filter(pk=exam_record_id).first()
        exam_record.answer = request.POST.get('answer','')
        exam_record.grade = request.POST.get('grade', '')
        exam_record.save()
        content = {}
        content['success_change_msg'] = f'考试记录:修改成功'
        request.session['change_exam_record_content'] = content
        return redirect(reverse('exam_record'))

class QueryExamRecordView(View):  #查询试卷模板
    def get(self,request):
        content = {}
        content['all_levels'] = ('本科', '专科')
        content['all_subjects'] = ('英语', '语文', '生物', '化学')
        content['all_majors'] = ('软件工程', '法学', '数学')

        query_form = request.session.get('query_exam_record_form', {})
        exam_records = ExamRecord.objects.filter(user__level=query_form.get('level',''),
                                                 user__major=query_form.get('major',''),
                                                 exam__exam_template__subject=query_form.get('subject',''),
                                                 user__username__icontains=query_form.get('username',''),
                                                 user__idcard__icontains=query_form.get('idcard',''))


        content.update(get_model_list_data(request, exam_records))
        if not exam_records:  # 当返回 int 0时，返回empty_error 信息
            content['query_empty_error'] = f'该查询 {query_form}  ：结果为空'
        content['last_query_form'] = query_form
        return render(request, 'exam_record.html', content)
    def post(self,request):
        query = {}
        query['level'] = request.POST.get('level', '')
        query['subject'] = request.POST.get('subject', '')
        query['major'] = request.POST.get('major', '')
        query['username'] = request.POST.get('username', '')
        query['idcard'] = request.POST.get('idcard', '')
        request.session['query_exam_record_form'] = query
        return redirect(reverse('query_exam_record'))


class ExamGradeView(View):
    def get(self,request):
        if request.is_ajax():  #删除
            exam_record_id = request.GET.get('obj_unique', '')
            exam_record = ExamRecord.objects.filter(pk=exam_record_id).first()

            if exam_record:
                exam_record.delete()
                return SuccessResponse()
            else:
                return ErrorResponse('该考试成绩不存在')
        content = {}
        content['all_levels'] = ('本科','专科')
        content['all_subjects'] = ('英语', '语文', '生物', '化学')
        content['all_majors'] = ('软件工程','法学','数学')
        exam_records = ExamRecord.objects.all()
        content.update(get_model_list_data(request, exam_records))
        if request.session.get('change_exam_grade_content',''):
            content.update(request.session.get('change_exam_grade_content', {}))
            del request.session['change_exam_grade_content']
        return render(request, 'exam_grade.html', content)
    def post(self,request):    # ajax
        if request.is_ajax():
            data = {}
            level = request.POST.get('level', '')
            major = request.POST.get('major', '')
            subject = request.POST.get('subject', '')
            username = request.POST.get('username', '')
            idcard = request.POST.get('idcard', '')
            exam_records = ExamRecord.objects.filter(user__level=level,user__major=major,user__username__icontains=username,
                                             user__idcard__icontains=idcard,exam__exam_template__subject=subject)

            data['exam_record_ls'] = []
            for exam_record in exam_records:
                dic = {}
                dic['username'] = exam_record.user.username
                dic['idcard'] = exam_record.user.idcard
                dic['level'] = exam_record.user.level
                dic['major'] = exam_record.user.major
                dic['subject'] = exam_record.exam.exam_template.subject
                dic['exam_record_id'] = exam_record.id
                dic['grade'] = exam_record.grade
                data['exam_record_ls'].append(dic)
            data['status'] = 'SUCCESS'
            data['exam_record_num'] = len(exam_records)
            return JsonResponse(data)
        else:
            exam_record_id = request.POST.get('exam_record_id', '')
            exam_record = ExamRecord.objects.filter(pk=exam_record_id).first()
            exam_record.grade = request.POST.get('grade', '')
            exam_record.save()
            content = {}
            content['success_change_msg'] = f'考试成绩:修改成功'
            request.session['change_exam_grade_content'] = content
            return redirect(reverse('exam_grade'))

class ExportView(View):
    def post(self,request):
        content = {}
        exam_record_id_ls = request.POST.getlist('item')  # 获取该多选框的所有选中的值组成的列表
        if exam_record_id_ls:
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment;filename=student_grade.xls'   #不知道为什么，中文名字不行【变成下载了】，英文就能设置
            # 创建一个文件对象
            wb = xlwt.Workbook(encoding='utf8')
            # 创建一个sheet对象
            sheet = wb.add_sheet('学生成绩表')
            # 写入文件标题
            sheet.write(0, 0, '姓名')
            sheet.write(0, 1, '身份证号')
            sheet.write(0, 2, '层次')
            sheet.write(0, 3, '专业')
            sheet.write(0, 4, '科目	')
            sheet.write(0, 5, '考试批次')
            sheet.write(0, 6, '成绩')


            for index,pk in enumerate(exam_record_id_ls):
                exam_record = ExamRecord.objects.filter(pk=pk).first()
                sheet.write(index+1, 0, exam_record.user.username)
                sheet.write(index+1, 1, exam_record.user.idcard)
                sheet.write(index+1, 2, exam_record.user.level)
                sheet.write(index+1, 3, exam_record.user.major)
                sheet.write(index+1, 4, exam_record.exam.exam_template.subject)
                sheet.write(index+1, 5, exam_record.exam.exam_template.exam_th)
                sheet.write(index+1, 6, exam_record.grade)

            # 写出到IO
            output = BytesIO()
            wb.save(output)
            # 重新定位到开始
            output.seek(0)
            response.write(output.getvalue())
            content['export_success_msg'] = f'导出{len(exam_record_id_ls)}个学生考试记录信息'
            return response
        else:
            content['export_error_msg'] = '没有选中考试记录，导出失败'
            request.session['change_exam_grade_content'] = content
            return redirect(reverse('exam_grade'))
class QueryExamGradeView(View):
    def get(self,request):
        content = {}
        content['all_levels'] = ('本科', '专科')
        content['all_subjects'] = ('英语', '语文', '生物', '化学')
        content['all_majors'] = ('软件工程', '法学', '数学')

        query_form = request.session.get('query_exam_record_form', {})
        exam_records = ExamRecord.objects.filter(user__level=query_form.get('level',''),
                                                 user__major=query_form.get('major',''),
                                                 exam__exam_template__subject=query_form.get('subject',''),
                                                 user__username__icontains=query_form.get('username',''),
                                                 user__idcard__icontains=query_form.get('idcard',''))


        content.update(get_model_list_data(request, exam_records))
        if not exam_records:  # 当返回 int 0时，返回empty_error 信息
            content['query_empty_error'] = f'该查询 {query_form}  ：结果为空'
        content['last_query_form'] = query_form
        return render(request, 'exam_grade.html', content)
    def post(self,request):
        query = {}
        query['level'] = request.POST.get('level', '')
        query['subject'] = request.POST.get('subject', '')
        query['major'] = request.POST.get('major', '')
        query['username'] = request.POST.get('username', '')
        query['idcard'] = request.POST.get('idcard', '')
        request.session['query_exam_record_form'] = query
        return redirect(reverse('query_exam_grade'))

# def export_excel(request):
#     # 设置HTTPResponse的类型
#     response = HttpResponse(content_type='application/vnd.ms-excel')
#     response['Content-Disposition'] = 'attachment;filename=学生成绩表.xls'
#     # 创建一个文件对象
#     wb = xlwt.Workbook(encoding='utf8')
#     # 创建一个sheet对象
#     sheet = wb.add_sheet('exam_record_sheet')
#
#     # 设置文件头的样式,这个不是必须的可以根据自己的需求进行更改
#     style_heading = xlwt.easyxf("""
#                 font:
#                     name Arial,
#                     colour_index white,
#                     bold on,
#                     height 0xA0;
#                 align:
#                     wrap off,
#                     vert center,
#                     horiz center;
#                 pattern:
#                     pattern solid,
#                     fore-colour 0x19;
#                 borders:
#                     left THIN,
#                     right THIN,
#                     top THIN,
#                     bottom THIN;
#                 """)
#
#     # 写入文件标题
#     sheet.write(0, 0, '申请编号', style_heading)
#     sheet.write(0, 1, '客户名称', style_heading)
#     sheet.write(0, 2, '联系方式', style_heading)
#     sheet.write(0, 3, '身份证号码', style_heading)
#     sheet.write(0, 4, '办理日期', style_heading)
#     sheet.write(0, 5, '处理人', style_heading)
#     sheet.write(0, 6, '处理状态', style_heading)
#     sheet.write(0, 7, '处理时间', style_heading)
#
#     # 写出到IO
#     output = BytesIO()
#     wb.save(output)
#     # 重新定位到开始
#     output.seek(0)
#     response.write(output.getvalue())
#     return response


