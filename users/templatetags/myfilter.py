from django import template
from users.models import Question
import json

register = template.Library()

@register.filter
def split_self(value,index):
    ls = value.split('\n')
    print(value)
    print(ls)
    return ls[index]

@register.filter
def get_range(value):
    ls = []
    for i in range(int(value)):
        ls.append(i)
    return ls

@register.filter
def parse_dict_str(value):
    dic = json.loads(value)  #教学：：只有dumps后的字符串才能进行loads，否则报错，直接将dict str的字符串也会报错
    single_choice_id_ls = dic['single_choice_id_ls']
    mul_choice_id_ls = dic['mul_choice_id_ls']
    judge_id_ls = dic['judge_id_ls']
    all_questions = {'single_choice_id_ls':[],'mul_choice_id_ls':[],'judge_id_ls':[]}
    for pk in single_choice_id_ls:
        all_questions['single_choice_id_ls'].append(Question.objects.filter(pk=pk).first())
    for pk in mul_choice_id_ls:
        all_questions['mul_choice_id_ls'].append(Question.objects.filter(pk=pk).first())
    for pk in judge_id_ls:
        all_questions['judge_id_ls'].append(Question.objects.filter(pk=pk).first())
    print(value)
    print(all_questions)
    return all_questions

@register.filter
def dictToLs(value):
    ls = []
    for k,v in value.items():
        tup = (k,v)
        ls.append(tup)
    print(type(value), value)
    print(ls)
    return ls

