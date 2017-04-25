#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: __init__.py.py
@time: 2017/3/10 下午10:48
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


class SelectAreaCodeWidget(object):
    """
    自定义选择组件 - 区号
    """
    def __call__(self, field, **kwargs):
        params = {
            'id': field.id,
            'name': field.id,
            'class': 'selectpicker show-tick',
            'data-live-search': 'true',
            'title': 'Choose one of the following...',
            'data-header': 'Select a condiment',
        }
        html = ['<select %s>' % html_params(**params)]
        for _, area_data in field.choices:
            for area_name, area_list in area_data.items():
                html.append('\t<optgroup label="%s">' % area_name)
                for country_data in area_list:
                    # html.append('\t\t<option value="%s" data-subtext="%s(%s)">[%s] %s</option>' % (country_data['id'], country_data['name_c'], country_data['name_e'], country_data['short_code'], country_data['phone_pre']))
                    html.append('\t\t<option value="%s" data-subtext="%s">[%s] %s</option>' % (country_data['id'], country_data['name_c'], country_data['short_code'], country_data['phone_pre']))
                html.append('\t</optgroup>')
        html.append('</select>')
        return HTMLString('\n'.join(html))


class SelectAreaCode(SelectField):
    """
    自定义选择表单控件
    """
    widget = SelectAreaCodeWidget()

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
