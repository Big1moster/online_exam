from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.utils import timezone

# Create your models here.
class Knowledge(models.Model):
    knowledge_name = models.CharField(max_length=128)
    subject_choice = (
        ('英语', '英语'),
        ('语文', '语文'),
        ('生物', '生物'),
        ('化学', '化学')
    )
    subject = models.CharField(max_length=32, choices=subject_choice, default='英语')
    level_choice = (
        ('本科', '本科'),
        ('专科', '专科')
    )
    level = models.CharField(max_length=32, choices=level_choice, default='本科')  # 层次（本科、专科）
    major_choice = (
        ('软件工程', '软件工程'),
        ('法学', '法学'),
        ('数学', '数学')
    )
    major = models.CharField(max_length=32, choices=major_choice, default='软件工程')  # 专业
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    last_updated_time = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.knowledge_name

    class Meta:
        db_table = 'knowledge'
        ordering = ['-last_updated_time']
        verbose_name = '知识点'
        verbose_name_plural = verbose_name



class Plan(models.Model):
    plan_name = models.CharField(max_length=32,unique=True)
    single_choice_num = models.IntegerField(default=0)  #在HTML中表现为NumberInput标签。
    single_choice_score = models.IntegerField(default=0)
    mul_choice_num = models.IntegerField(default=0)
    mul_choice_score = models.IntegerField(default=0)
    judge_num = models.IntegerField(default=0)
    judge_score = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    last_updated_time = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return "<Plan: %s>" % self.plan_name

    def get_total_score(self):  # 自定义方法获取该对象的总分  在模板中需要这样访问# {{plan_editor.total_score}} {{plan_editor.get_total_score}}
        total_score = self.single_choice_num*self.single_choice_score + self.mul_choice_num*self.mul_choice_score +self.judge_num*self.judge_score
        return total_score

    total_score = property(get_total_score) #使用属性方式访问该方法

    class Meta:
        ordering = ['-last_updated_time']
        verbose_name = '试卷方案'
        verbose_name_plural = verbose_name

class UserProfile(AbstractUser): #用户表
    username = models.CharField(max_length=32,unique=True)
    idcard = models.CharField(max_length=32,unique=True,null=True)  #身份证号码
    password = models.CharField(max_length=128,default='zxcdsf789')
    level_choice = (
        ('本科','本科'),
        ('专科','专科')
    )
    level = models.CharField(max_length=32,choices=level_choice,default='本科')  #层次（本科、专科）
    major_choice = (
        ('软件工程','软件工程'),
        ('法学','法学'),
        ('数学','数学')
    )
    major = models.CharField(max_length=32,choices=major_choice,default='软件工程')  #专业
    role_choice = (
        ('student','学生'),
        ('teacher','教师'),
        ('administrator','管理员')
    )
    role = models.CharField(max_length=32,choices=role_choice,default='student')  #角色（学生、教师、管理员）
    is_checked = models.BooleanField(default=False) #是否审核
    touxiang = models.ImageField(upload_to='images/%Y/%m',default='images/2019/12/touxiang_img.png',max_length=100)
    email = models.EmailField(blank=True,null=True)
    create_time = models.DateTimeField(auto_now_add=True) #创建时间
    last_updated_time = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        return "<User: %s>" % self.username

    def get_old(self):  #自定义方法获取该对象的岁数信息,模板语法中只能使用这种没有参数得到方法
        # 362502199702062658
        old = self.idcard[6:10]
        return datetime.now().year-int(old)

    class Meta:
        db_table = 'auth_user'
        ordering = ['-last_updated_time']
        verbose_name = '用户数据表'
        verbose_name_plural = verbose_name

class Question(models.Model):
    question_name = models.TextField()
    option = models.TextField()
    answer = models.CharField(max_length=8)
    score = models.IntegerField()

    subject_choice = (
        ('英语', '英语'),
        ('语文', '语文'),
        ('生物', '生物'),
        ('化学', '化学')
    )
    subject = models.CharField(max_length=32, choices=subject_choice, default='英语')
    question_type_choice = (
        ('单选题', '单选题'),
        ('多选题', '多选题'),
        ('判断题', '判断题')
    )
    question_type = models.CharField(max_length=32, choices=question_type_choice, default='单选题')
    difficult_choice = (
        ('简单', '简单'),
        ('一般', '一般'),
        ('困难', '困难'),
        ('极难', '极难')
    )
    difficult = models.CharField(max_length=32, choices=difficult_choice, default='一般')
    knowledge = models.ForeignKey(Knowledge,on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    last_updated_time = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.question_name

    class Meta:
        db_table = 'question'
        ordering = ['-last_updated_time']
        verbose_name = '问题'
        verbose_name_plural = verbose_name

class ExamTemplate(models.Model):
    exam_template_name = models.CharField(max_length=32,unique=True)
    exam_name = models.CharField(max_length=32,unique=True)
    exam_th = models.IntegerField(default=0)
    subject_choice = (
        ('英语','英语'),
        ('语文','语文'),
        ('生物', '生物'),
        ('化学', '化学')
    )
    subject = models.CharField(max_length=32,choices=subject_choice,default='英语')
    difficult_choice = (
        ('简单','简单'),
        ('一般','一般'),
        ('困难', '困难'),
        ('极难', '极难')
    )
    difficult = models.CharField(max_length=32, choices=difficult_choice, default='一般')
    plan = models.ForeignKey(Plan,on_delete=models.CASCADE)    # 删除外键该字段页跟着呗删除
    exam_start_time = models.DateTimeField(default=timezone.now)  #在对象的创建时间默认被设置为当前值，能在日后修改它
    exam_end_time = models.DateTimeField(default=timezone.now)
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    last_updated_time = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return "<ExamTemplate: %s>" % self.exam_template_name

    def get_exam_time(self):  #自定义方法获取 考试时长/分
        exam_time = (self.exam_end_time - self.exam_start_time).seconds//60            #两时间相减得到<class 'datetime.timedelta'>,得到整数秒，再得到分钟
        return exam_time

    class Meta:
        ordering = ['-last_updated_time']
        verbose_name = '试卷模板'
        verbose_name_plural = verbose_name

class Exam(models.Model):
    exam_template = models.ForeignKey(ExamTemplate,on_delete=models.CASCADE)
    exam_describe = models.TextField(default='')   #中途增加的字段需要设置默认值，因为部分已存在的记录没有该字段
    exam_name = models.CharField(max_length=32,default='测试试卷')
    question_id_ls = models.CharField(max_length=128,default="{'single_choice_id_ls': [], 'mul_choice_id_ls': [],'judge_id_ls': []}")
    major_choice = (
        ('软件工程', '软件工程'),
        ('法学', '法学'),
        ('数学', '数学')
    )
    major = models.CharField(max_length=32, choices=major_choice, default='软件工程')  # 专业
    level_choice = (
        ('本科', '本科'),
        ('专科', '专科')
    )
    level = models.CharField(max_length=32, choices=level_choice, default='本科')  # 层次（本科、专科）
    allot = models.ManyToManyField(UserProfile,related_name='allot_set')
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    last_updated_time = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"<Exam: {self.exam_template}-{self.major}-{self.level}>"

    def get_single_choice_num(self):  #自定义方法获取
        single_choice_num = self.exam_template.plan.single_choice_num
        return single_choice_num

    def get_mul_choice_num(self):
        mul_choice_num = self.exam_template.plan.mul_choice_num
        return mul_choice_num

    def get_judge_num(self):
        judge_num = self.exam_template.plan.judge_num
        return judge_num

    def get_total_num(self):
        total_num = self.get_single_choice_num()+self.get_mul_choice_num()+self.get_judge_num()
        return total_num

    def get_total_score(self):
        total_score = self.exam_template.plan.total_score
        return total_score

    class Meta:
        ordering = ['-last_updated_time']
        verbose_name = '试卷'
        verbose_name_plural = verbose_name

class ExamRecord(models.Model):
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    answer = models.CharField(max_length=128,null=True,blank=True)
    grade = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    last_updated_time = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"<ExamRecord: {self.exam.exam_name}-{self.user.username}>"


    class Meta:
        ordering = ['-last_updated_time']
        verbose_name = '考试记录表'
        verbose_name_plural = verbose_name