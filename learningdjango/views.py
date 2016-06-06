# coding:utf-8
from django.shortcuts import render

from learningdjango.forms import AddForm

'处理用户发出的请求，从urls.py中对应过来, 通过渲染templates中的网页可以将显示内容，比如登陆后的用户名，用户请求的数据，输出到网页。'
# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse(u'欢迎光临')


def home(request):
    return render(request, 'learn/home.html')


def add(request):
    # a = request.GET['a']
    # b = request.GET['b']
    a = request.GET.get('a', 0)  # default 0
    b = request.GET.get('b', 0)  # default 0
    c = int(a) + int(b)
    return HttpResponse(str(c))


# e.g. 127.0.0.1:8000/add/3/4
def add2(request, a, b):
    c = int(a) + int(b)
    return HttpResponse(str(c))


def index2(request):
    return render(request,'learn/inputnumber.html')


def add3(request):
    a = request.GET['a']
    b = request.GET['b']
    a = int(a)
    b = int(b)
    return HttpResponse(str(a + b))


def postadd(request):
    if request.method == 'POST':# 当提交表单时

        form = AddForm(request.POST) # form 包含提交的数据

        if form.is_valid():# 如果提交的数据合法
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
            return HttpResponse(str(int(a) + int(b)))

    else:# 当正常访问时
        form = AddForm()
    return render(request, 'learn/postcalc.html', {'form': form})

