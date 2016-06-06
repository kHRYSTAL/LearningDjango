#!/usr/bin/env python3
# -*- coding:utf-8 -*-


"""
@version: ??
@usage: 
@author: kHRYSTAL
@license: Apache Licence 
@contact: khrystal0918@gmail.com
@site: https://github.com/kHRYSTAL
@software: PyCharm
@file: forms.py
@time: 16/6/6 下午2:48
"""

from django import forms

'''
表单中的数据
'''

class AddForm(forms.Form):
    a = forms.IntegerField()
    b = forms.IntegerField()