import ast

from django.db import models

# Create your models here.

'''
name 和 age 等字段中不能有 __（双下划线，因为在Django QuerySet API中有特殊含义
（用于关系，包含，不区分大小写，以什么开头或结尾，日期的大于小于，正则等）

也不能有Python中的关键字，name 是合法的，student_name 也合法，
但是student__name不合法，try, class, continue 也不合法，因为它是Python的关键字( import keyword; print(keyword.kwlist) 可以打出所有的关键字)
'''


class Person(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    grade = models.IntegerField()

    def __str__(self):
        return self.name

    __repr__ = __str__

'''
#192:StartDjango kHRYSTAL$ python3 manage.py makemigrations
Migrations for 'learningdjango':
  0001_initial.py:
    - Create model Person
#192:StartDjango kHRYSTAL$ python3 manage.py migrate
Operations to perform:
  Apply all migrations: contenttypes, auth, sessions, learningdjango, admin
Running migrations:
  Rendering model states... DONE
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying learningdjango.0001_initial... OK
  Applying sessions.0001_initial... OK
'''

'''
192:StartDjango kHRYSTAL$ python3 manage.py shell
Python 3.5.0 (v3.5.0:374f501f4567, Sep 12 2015, 11:00:19)
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from learningdjango.models import Person
>>> Person.objects.create(name='YYG', age=25)

>>> Person.objects.get(name='A')
Traceback (most recent call last):
  File "/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/site-packages/django/core/management/commands/shell.py", line 69, in handle
    self.run_shell(shell=options['interface'])
  File "/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/site-packages/django/core/management/commands/shell.py", line 61, in run_shell
    raise ImportError
ImportError

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/site-packages/django/db/models/manager.py", line 122, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/Library/Frameworks/Python.framework/Versions/3.5/lib/python3.5/site-packages/django/db/models/query.py", line 387, in get
    self.model._meta.object_name
learningdjango.models.DoesNotExist: Person matching query does not exist.
>>> Person.objects.get(name='YYG')
>>> Person.objects.get(name='YYG')
'''

'''
when add __str__ method;
>>> from learningdjango.models import Person
>>> Person.objects.get(name='YYG')
<Person: YYG>

'''

'''
新建一个对象的方法有以下几种：

Person.objects.create(name=name,age=age)

p = Person(name="WZ", age=23)

p.save()

p = Person(name="TWZ")

p.age = 23

p.save()

Person.objects.get_or_create(name="WZT", age=23)

这种方法是防止重复很好的方法，但是速度要相对慢些，返回一个元组，第一个为Person对象，第二个为True或False, 新建时返回的是True, 已经存在时返回False.
'''

'''
获取对象有以下方法：

Person.objects.all()

Person.objects.all()[:10] 切片操作，获取10个人，不支持负索引，切片可以节约内存

Person.objects.get(name=name)

get是用来获取一个对象的，如果需要获取满足条件的一些人，就要用到filter

Person.objects.filter(name="abc") # 等于Person.objects.filter(name__exact="abc") 名称严格等于 "abc" 的人

Person.objects.filter(name__iexact="abc") # 名称为 abc 但是不区分大小写，可以找到 ABC, Abc, aBC，这些都符合条件



Person.objects.filter(name__contains="abc") # 名称中包含 "abc"的人

Person.objects.filter(name__icontains="abc") #名称中包含 "abc"，且abc不区分大小写



Person.objects.filter(name__regex="^abc") # 正则表达式查询

Person.objects.filter(name__iregex="^abc")# 正则表达式不区分大小写

filter是找出满足条件的，当然也有排除符合某条件的

Person.objects.exclude(name__contains="WZ") # 排除包含 WZ 的Person对象

Person.objects.filter(name__contains="abc").exclude(age=23) # 找出名称含有abc, 但是排除年龄是23岁的
'''
# CustomField
# 减少文本的长度，保存数据的时候压缩，读取的时候解压缩，如果发现压缩后更长，就用原文本直接存储：
class CompressedTextField(models.TextField):
    """
    model Fields for storing text in a compressed format (bz2 by default)
    """

    def from_db_value(self, value, expression, connection, context):
        if not value:
            return value
        try:
            return value.decode('base64').decode('bz2').decode('utf-8')
        except Exception:
            return value

    def to_python(self, value):
        if not value:
            return value
        try:
            return value.decode('base64').decode('bz2').decode('utf-8')
        except Exception:
            return value

    def get_prep_value(self, value):
        if not value:
            return value
        try:
            value.decode('base64')
            return value
        except Exception:
            try:
                return value.encode('utf-8').encode('bz2').encode('base64')
            except Exception:
                return value
'''
to_python 函数用于转化数据库中的字符到 Python的变量， get_prep_value 用于将Python变量处理后(此处为压缩）保存到数据库，使用和Django自带的 Field 一样。
'''

# 比如我们想保存一个 列表到数据库中，在读取用的时候要是 Python的列表的形式，我们来自己写一个 ListField：
class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return str(value) # use str(value) in Python 3

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

'''
>>> from blog.models import Article

>>> a = Article()
>>> a.labels.append('Django')
>>> a.labels.append('custom fields')

>>> a.labels
['Django', 'custom fields']

>>> type(a.labels)
<type 'list'>

>>> a.content = u'我正在写一篇关于自定义Django Fields的教程'
>>> a.save()
'''