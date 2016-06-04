# coding:utf-8
from django.shortcuts import render
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