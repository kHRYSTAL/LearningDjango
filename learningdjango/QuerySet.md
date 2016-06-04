Django 模型中我们学习了一些基本的创建与查询。这里专门来讲一下数据库接口相关的接口（QuerySet API)，当然您也可以选择暂时跳过此节，如果以后用到数据库相关的时候再看也是可以的。

从数据库中查询出来的结果一般是一个集合，这个集合叫做 QuerySet。

文中的例子大部分是基于这个 blog/models.py

from django.db import models


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __unicode__(self):  # __str__ on Python 3
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __unicode__(self):  # __str__ on Python 3
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    n_comments = models.IntegerField()
    n_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __unicode__(self):  # __str__ on Python 3
        return self.headline
1. QuerySet 创建对象的方法

>>> from blog.models import Blog
>>> b = Blog(name='Beatles Blog', tagline='All the latest Beatles news.')
>>> b.save()

总之，一共有四种方法
# 方法 1
Author.objects.create(name="WeizhongTu", email="tuweizhong@163.com")

# 方法 2
twz = Author(name="WeizhongTu", email="tuweizhong@163.com")
twz.save()

# 方法 3
twz = Author()
twz.name="WeizhongTu"
twz.email="tuweizhong@163.com"

# 方法 4，首先尝试获取，不存在就创建，可以防止重复
Author.objects.get_or_create(name="WeizhongTu", email="tuweizhong@163.com")
# 返回值(object, True/False)
备注：前三种方法返回的都是对应的 object，最后一种方法返回的是一个元组，(object, True/False)，创建时返回 True, 已经存在时返回 False



当有一对多，多对一，或者多对多的关系的时候，先把相关的对象查询出来


>>> from blog.models import Entry
>>> entry = Entry.objects.get(pk=1)
>>> cheese_blog = Blog.objects.get(name="Cheddar Talk")
>>> entry.blog = cheese_blog
>>> entry.save()


2. 获取对象的方法（上一篇的部分代码）

Person.objects.all() # 查询所有
Person.objects.all()[:10] 切片操作，获取10个人，不支持负索引，切片可以节约内存，不支持负索引，后面有相应解决办法，第7条
Person.objects.get(name="WeizhongTu") # 名称为 WeizhongTu 的一条，多条会报错

get是用来获取一个对象的，如果需要获取满足条件的一些人，就要用到filter
Person.objects.filter(name="abc") # 等于Person.objects.filter(name__exact="abc") 名称严格等于 "abc" 的人
Person.objects.filter(name__iexact="abc") # 名称为 abc 但是不区分大小写，可以找到 ABC, Abc, aBC，这些都符合条件

Person.objects.filter(name__contains="abc") # 名称中包含 "abc"的人
Person.objects.filter(name__icontains="abc") #名称中包含 "abc"，且abc不区分大小写

Person.objects.filter(name__regex="^abc") # 正则表达式查询
Person.objects.filter(name__iregex="^abc")# 正则表达式不区分大小写

# filter是找出满足条件的，当然也有排除符合某条件的
Person.objects.exclude(name__contains="WZ") # 排除包含 WZ 的Person对象
Person.objects.filter(name__contains="abc").exclude(age=23) # 找出名称含有abc, 但是排除年龄是23岁的
3. QuerySet 是可迭代的，比如：


es = Entry.objects.all()
for e in es:
    print(e.headline)
Entry.objects.all() 或者 es 就是 QuerySet 是查询所有的 Entry 条目。

注意事项：

(1). 如果只是检查 Entry 中是否有对象，应该用 Entry.objects.all().exists()

(2). QuerySet 支持切片 Entry.objects.all()[:10] 取出10条，可以节省内存

(3). 用 len(es) 可以得到Entry的数量，但是推荐用 Entry.objects.count()来查询数量，后者用的是SQL：SELECT COUNT(*)

(4). list(es) 可以强行将 QuerySet 变成 列表

4. QuerySet 是可以用pickle序列化到硬盘再读取出来的

>>> import pickle
>>> query = pickle.loads(s)     # Assuming 's' is the pickled string.
>>> qs = MyModel.objects.all()
>>> qs.query = query            # Restore the original 'query'.
5. QuerySet 查询结果排序

作者按照名称排序

Author.objects.all().order_by('name')
Author.objects.all().order_by('-name') # 在 column name 前加一个负号，可以实现倒序
6. QuerySet 支持链式查询

Author.objects.filter(name__contains="WeizhongTu").filter(email="tuweizhong@163.com")
Author.objects.filter(name__contains="Wei").exclude(email="tuweizhong@163.com")

# 找出名称含有abc, 但是排除年龄是23岁的
Person.objects.filter(name__contains="abc").exclude(age=23)
7. QuerySet 不支持负索引


Person.objects.all()[:10] 切片操作，前10条
Person.objects.all()[-10:] 会报错！！！

# 1. 使用 reverse() 解决
Person.objects.all().reverse()[:2] # 最后两条
Person.objects.all().reverse()[0] # 最后一条

# 2. 使用 order_by，在栏目名（column name）前加一个负号
Author.objects.order_by('-id')[:20] # id最大的20条

8. QuerySet 重复的问题，使用 .distinct() 去重

一般的情况下，QuerySet 中不会出来重复的，重复是很罕见的，但是当跨越多张表进行检索后，结果并到一起，可以会出来重复的值（我最近就遇到过这样的问题）


qs1 = Pathway.objects.filter(label__name='x')
qs2 = Pathway.objects.filter(reaction__name='A + B >> C')
qs3 = Pathway.objects.filter(inputer__name='WeizhongTu')

# 合并到一起
qs = qs1 | qs2 | qs3
这个时候就有可能出现重复的

# 去重方法
qs = qs.distinct()




最后更新 2015.12.22 未完待续。。



参考：

Django数据库操作官方文档： QuerySet API: https://docs.djangoproject.com/en/dev/ref/models/querysets/