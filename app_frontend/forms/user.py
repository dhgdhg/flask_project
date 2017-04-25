#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: user.py
@time: 2017/3/17 下午11:49
"""


from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, BooleanField, DateField, DateTimeField, HiddenField
from wtforms.validators import DataRequired, Length, NumberRange, EqualTo, Email, ValidationError, IPAddress
from app_frontend.api.user_auth import get_user_auth_row


def reg_email_repeat(form, field):
    """
    邮箱重复校验
    """
    condition = {
        'auth_type': 'email',
        'auth_key': field.data
    }
    row = get_user_auth_row(**condition)
    if row:
        raise ValidationError(u'注册邮箱重复')


class UserProfileForm(Form):
    """
    用户基本信息表单
    """
    id = HiddenField('User Id', validators=[DataRequired()])
    user_pid = HiddenField('User Pid', validators=[DataRequired()])
    nickname = StringField('Nick Name', validators=[DataRequired(), Length(min=2, max=20)])
    avatar_url = StringField('Avatar Url')
    email = StringField('Email', validators=[DataRequired()])
    area_code = StringField('Area Code')
    phone = StringField('Phone')
    birthday = DateField('Birthday')
    id_card = StringField('ID Card')
    create_time = DateTimeField('Create Time')
    update_time = DateTimeField('Update Time')
    last_ip = StringField('Last Ip', validators=[IPAddress()])


class EditPassword(Form):
    """
    修改用户密码
    """
    password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=6, max=40),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password', validators=[
        DataRequired(),
        Length(min=6, max=40)
    ])
