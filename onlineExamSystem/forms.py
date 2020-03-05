from django import forms
from users.models import UserProfile,Plan,ExamTemplate,Question,Knowledge
from django.contrib import auth

class EditorQuestionForm(forms.Form):
    old_question_name = forms.Textarea()
    questionNname = forms.Textarea()

    answer = forms.CharField(max_length=8, min_length=1)
    subject = forms.CharField(max_length=32)
    question_type = forms.CharField(max_length=32)
    difficult = forms.CharField(max_length=32)
    knowledge_name = forms.CharField(max_length=128)
    score = forms.CharField(max_length=2)

    # def clean_questionNname(self): #无法进行验证？？？why
    #     old_question_name = self.data.get('old_question_name','')
    #     questionNname = self.cleaned_data['questionNname']
    #     if questionNname == old_question_name:
    #         return questionNname
    #     elif Question.objects.filter(question_name = questionNname).exists():
    #         raise forms.ValidationError('问题已存在')
    #     else:
    #         return questionNname

    def clean_score(self):
        score = self.cleaned_data['score']
        if score.isdigit():  # bool是否只包含数字
            return score
        else:
            raise forms.ValidationError('分数只能是数字')

    def clean_subject(self):
        subject_ls = ('英语', '语文', '生物', '化学', '数学')
        subject = self.cleaned_data['subject']
        if subject not in subject_ls:
            raise forms.ValidationError('该科目不存在')
        else:
            return subject

    def clean_question_type(self):
        question_type_ls = ('单选题', '多选题', '判断题')
        question_type = self.cleaned_data['question_type']
        if question_type not in question_type_ls:
            raise forms.ValidationError('该题型不存在')
        else:
            return question_type

    def clean_difficult(self):
        difficult_ls = ('简单', '一般', '困难', '极难')
        difficult = self.cleaned_data['difficult']
        if difficult not in difficult_ls:
            raise forms.ValidationError('该难度不存在')
        else:
            return difficult


class QuestionInfoForm(forms.Form):
    question_name = forms.Textarea()
    answer = forms.CharField(max_length=8,min_length=1)
    subject = forms.CharField(max_length=32)
    question_type = forms.CharField(max_length=32)
    difficult = forms.CharField(max_length=32)
    knowledge_name = forms.CharField(max_length=128)
    score = forms.CharField(max_length=2)

    def clean_score(self):
        score = self.cleaned_data['score']
        if score.isdigit(): #bool是否只包含数字
            return score
        else:
            raise forms.ValidationError('分数只能是数字')

    def clean_subject(self):
        subject_ls = ('英语', '语文','生物','化学','数学')
        subject = self.cleaned_data['subject']
        if subject not in subject_ls:
            raise forms.ValidationError('该科目不存在')
        else:
            return subject

    def clean_question_type(self):
        question_type_ls = ('单选题','多选题','判断题')
        question_type = self.cleaned_data['question_type']
        if question_type not in question_type_ls:
            raise forms.ValidationError('该题型不存在')
        else:
            return question_type
    def clean_difficult(self):
        difficult_ls = ('简单', '一般', '困难', '极难')
        difficult = self.cleaned_data['difficult']
        if difficult not in difficult_ls:
            raise forms.ValidationError('该难度不存在')
        else:
            return difficult


class ChangeUserInfoForm(forms.Form):

    username = forms.CharField(max_length=20, min_length=3)
    idcard = forms.CharField(max_length=18, min_length=18)
    email = forms.EmailField(required=False)  #设置可为空

    # old_username = forms.CharField(max_length=20, min_length=3)
    # old_idcard = forms.CharField(max_length=18, min_length=18)
    # old_email = forms.EmailField()

    def clean_username(self):
        old_username = self.data.get('old_username','')
        username = self.cleaned_data['username']
        if old_username == username:
            return username
        elif UserProfile.objects.filter(username = username).exists():
            raise forms.ValidationError('用户名已存在')
        else:
            return username

    def clean_idcard(self):
        old_idcard = self.data.get('old_idcard','')
        idcard = self.cleaned_data['idcard']
        if old_idcard == idcard:
            return idcard
        elif UserProfile.objects.filter(idcard=idcard).exists():
            raise forms.ValidationError('该身份证已注册')
        else:
            return idcard

    def clean_email(self):
        old_email = self.data.get('old_email','')
        email = self.cleaned_data['email']
        if old_email == email:
            return email
        elif UserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已注册')
        else:
            return email
class EditorExamTemplateForm(forms.Form):
    old_exam_template_name = forms.CharField(max_length=32,min_length=3)
    exam_template_name = forms.CharField(max_length=32,min_length=3)
    exam_name = forms.CharField(max_length=32, min_length=3)
    old_exam_name = forms.CharField(max_length=32, min_length=3)

    def clean_exam_template_name(self):
        print(self.cleaned_data, self.data)
        exam_template_name = self.cleaned_data['exam_template_name']
        old_exam_template_name = self.cleaned_data['old_exam_template_name']

        if old_exam_template_name == exam_template_name:
            return exam_template_name
        elif ExamTemplate.objects.filter(exam_template_name=exam_template_name).exists():
            raise forms.ValidationError('试卷模板已存在')
        else:
            return exam_template_name

    def clean_exam_name(self):
        print(self.cleaned_data, self.data)
        exam_name = self.cleaned_data['exam_name']
        old_exam_name = self.data.get('old_exam_name','')
        print(old_exam_name)
        if old_exam_name == exam_name:
            return exam_name
        elif ExamTemplate.objects.filter(exam_name=exam_name).exists():
            raise forms.ValidationError('考试名称已存在')
        else:
            return exam_name

class AddExamTemplateForm(forms.Form):
    exam_template_name = forms.CharField(max_length=32,min_length=3)
    exam_name = forms.CharField(max_length=32, min_length=3)
    def clean_exam_template_name(self):
        exam_template_name = self.cleaned_data['exam_template_name']
        if ExamTemplate.objects.filter(exam_template_name = exam_template_name).exists():
            raise forms.ValidationError(f'该试卷模板：{exam_template_name} ；已存在')
        else:
            return exam_template_name
    def clean_exam_name(self):
        exam_name = self.cleaned_data['exam_name']
        if ExamTemplate.objects.filter(exam_name = exam_name).exists():
            raise forms.ValidationError(f'该考试名：{exam_name} ；已存在')
        else:
            return exam_name

class AddPlanForm(forms.Form):
    plan_name = forms.CharField(max_length=20, min_length=3)
    def clean_plan_name(self):
        plan_name = self.cleaned_data['plan_name']
        if Plan.objects.filter(plan_name = plan_name).exists():
            raise forms.ValidationError('方案名已存在')
        else:
            return plan_name

class EditorPlanForm(forms.Form):
    old_plan_name = forms.CharField(max_length=20, min_length=3)
    plan_name = forms.CharField(max_length=20, min_length=3)


    def clean_plan_name(self):
        plan_name = self.cleaned_data['plan_name']
        old_plan_name = self.cleaned_data['old_plan_name']
        if old_plan_name == plan_name:
            return plan_name
        elif Plan.objects.filter(plan_name = plan_name).exists():
            raise forms.ValidationError('方案名已存在')
        else:
            return plan_name

class EditorUserForm(forms.Form):
    old_username = forms.CharField(max_length=20, min_length=3)
    username = forms.CharField(max_length=20,min_length=3)
    old_idcard = forms.CharField(max_length=18,min_length=18)
    idcard = forms.CharField(max_length=18,min_length=18)
    level = forms.CharField(max_length=10)
    major = forms.CharField(max_length=32)
    role = forms.CharField(max_length=32)

#加下划线 专门正对字段进行验证
    def clean_username(self):
        old_username = self.cleaned_data['old_username']
        username = self.cleaned_data['username']
        if old_username == username:
            return username
        elif UserProfile.objects.filter(username = username).exists():
            raise forms.ValidationError('用户名已存在')
        else:
            return username


    def clean_idcard(self):
        old_idcard = self.cleaned_data['old_idcard']
        idcard = self.cleaned_data['idcard']
        if old_idcard == idcard:
            return idcard
        elif UserProfile.objects.filter(idcard=idcard).exists():
            raise forms.ValidationError('该身份证已注册')
        else:
            return idcard



class AddUserForm(forms.Form):
    username = forms.CharField(max_length=20,min_length=3)
    password = forms.CharField(max_length=32,min_length=6)
    idcard = forms.CharField(max_length=18,min_length=18)
    level = forms.CharField(max_length=10)
    major = forms.CharField(max_length=32)
    role = forms.CharField(max_length=32)

#加下划线 专门正对字段进行验证
    def clean_username(self):
        username = self.cleaned_data['username']
        if UserProfile.objects.filter(username = username).exists():
            raise forms.ValidationError('用户名已存在')
        else:
            return username


    def clean_idcard(self):
        idcard = self.cleaned_data['idcard']
        if UserProfile.objects.filter(idcard=idcard).exists():
            raise forms.ValidationError('该身份证已注册')
        else:
            return idcard
