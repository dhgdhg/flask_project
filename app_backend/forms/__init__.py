#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: __init__.py.py
@time: 2017/4/9 上午10:13
"""


from wtforms import SelectField
from wtforms.widgets import HTMLString
from wtforms.compat import text_type, iteritems
from wtforms.widgets import html_params


def select_multi_checkbox(field, ul_class='', **kwargs):
    """
    多选框控件
    :param field:
    :param ul_class:
    :param kwargs:
    :return:
    """
    kwargs.setdefault('type', 'checkbox')
    field_id = kwargs.pop('id', field.id)
    html = [u'<ul %s>' % html_params(id=field_id, class_=ul_class)]
    for value, label, checked in field.iter_choices():
        choice_id = u'%s-%s' % (field_id, value)
        options = dict(kwargs, name=field.name, value=value, id=choice_id)
        if checked:
            options['checked'] = 'checked'
        html.append(u'<li><input %s /> ' % html_params(**options))
        html.append(u'<label for="%s">%s</label></li>' % (field_id, label))
    html.append(u'</ul>')
    return u''.join(html)


class SelectBSWidget(object):
    """
    自定义选择组件
    """
    def __call__(self, field, **kwargs):
        params = {
            'id': field.id,
            'name': field.id,
            'class': 'selectpicker show-tick',
            # 'data-live-search': 'true',
            'title': kwargs.pop('placeholder') or 'Choose one of the following...',
            'data-header': kwargs.pop('data_header') or 'Select a condiment',
            'data-width': kwargs.pop('data_width') or 'auto'
        }
        html = ['<select %s>' % html_params(**params)]
        for k, v in field.choices:
            html.append('<option value="%s" data-subtext="[%s]">%s</option>' % (k, k, v))
        html.append('</select>')
        return HTMLString('\n'.join(html))


class SelectBS(SelectField):
    """
    自定义选择表单控件
    """
    widget = SelectBSWidget()

    def pre_validate(self, form):
        """
        校验表单传值是否合法
        """
        is_find = False
        for _, area_data in self.choices:
            for area_list in area_data.values():
                if self.data in [str(i['id']) for i in area_list]:
                    is_find = True
                    break
            if is_find:
                break
        else:
            raise ValueError(self.gettext('Not a valid choice'))

