# -*- coding:UTF-8 -*-
__autor__ = 'zhouli'
__date__ = '2019/9/5 22:22'
from django import forms
from django.forms import widgets
from cnblong.models import UserInfo
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError


class UserForm(forms.Form):
    user = forms.CharField(label="用户名", max_length=32, widget=widgets.TextInput(attrs={"class": "form-control"}),
                           error_messages={'required': '该字段不能为空'}
                           )
    pwd = forms.CharField(label="密码", max_length=32, widget=widgets.PasswordInput(attrs={"class": "form-control"}))
    re_pwd = forms.CharField(label="确认密码", max_length=32, widget=widgets.PasswordInput(attrs={"class": "form-control"}))
    email = forms.EmailField(label="邮箱", max_length=32, )

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_user(self):
        user = self.cleaned_data.get('user')  # 通过上面的校验
        users = UserInfo.objects.filter(username=user)
        if not users:
            return user
        else:
            raise ValidationError("该用户已注册！")

    def clean(self):
        pwd = self.cleaned_data.get("pwd")
        re_pwd = self.cleaned_data.get("re_pwd")
        if pwd and re_pwd:  # 没有通过校验的话就不判断2次密码一致了
            if pwd == re_pwd:
                return self.cleaned_data
            else:
                raise ValidationError("两次密码不一致！")
        else:
            return self.cleaned_data
