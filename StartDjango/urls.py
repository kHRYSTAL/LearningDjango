"""StartDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from learningdjango import views as learn_views  # new
'网址入口，关联到对应的views.py中的一个函数（或者generic类），访问网址就对应一个函数。'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', learn_views.index),  # new
    url(r'^add/$', learn_views.add, name='add'),  # calc
    url(r'^add2/(\d+)/(\d+)/$', learn_views.add2, name='add2'),
    url(r'^home/$', learn_views.home, name='home'),
    url(r'^index/$', learn_views.index2, name='index2'),
    url(r'^add3/$', learn_views.add3, name='add3'),
    url(r'^postc/$', learn_views.postadd, name='postadd'),
]

'''
name的作用:
1) 在模版中 可以使用{% url 'urlname' :param %}
加入url
如<a href="{% url 'add2' 4 5 %}">link</a>
渲染后为<a href="/add2/4/5/">link</a>

2) 当url的执行函数改为其他函数(参数没变), 可以不修改name
 直接在urls.py修改指定name的函数

3) 若url路径修改了 用户已经收藏了老url 可以在views中修改函数将网址跳转到新url
    def old_add2_redirect(request, a, b):
    return HttpResponseRedirect(
        reverse('add2', args=(a, b))
    )
    url(r'^add2/(\d+)/(\d+)/$', calc_views.old_add2_redirect),
    url(r'^new_add/(\d+)/(\d+)/$', calc_views.add2, name='add2'),
    假如用户收藏夹中有 /add2/4/5/ ，访问时就会自动跳转到新的 /new_add/4/5/ 了



'''
