from django import template
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime, timedelta
register = template.Library()


@register.simple_tag
def render_app_name(admin_cls):

    return admin_cls.model._meta.verbose_name


@register.simple_tag
def get_query_sets(admin_class):
    # print(admin_class.model.objects.all())
    return admin_class.model.objects.all()

@register.simple_tag
def build_table_row(request, obj, admin_class):
    # print(obj)
    # print(type(obj))
    row_ele = ""
    for index,column in enumerate(admin_class.list_display):
        # print("index",index)
        field_obj = obj._meta.get_field(column)
        # print(type(field_obj))
        # print(field_obj.choices)
        #处理choices的名称问题
        if field_obj.choices:
            column_data = getattr(obj, "get_%s_display"% column)()
            # print(type(column_data))
        else:
            column_data = getattr(obj,column)
        #处理时间的问题---侧面反映出写博客的重要性，可以抄过来嘛
        if type(column_data).__name__ == "datetime":
            column_data = column_data.strftime("%Y-%m-%d %H:%M:%S")

        if index == 0:
            column_data = "<a href='{request_path}{obj_id}/change/'>{data}</a>".format(request_path=request.path,
                                                                                       obj_id=obj.id,
                                                                                       data=column_data)
        row_ele += "<td>%s</td>"% column_data



    return mark_safe(row_ele)

# @register.simple_tag
# def render_page_ele(loop_counter, contacts, filter_conditions):
#     filters = ''
#     for k,v in filter_conditions.items():
#         filters += "&%s=%s"%(k,v)
#     if abs(contacts.number - loop_counter) <= 2:
#         ele_class = ""
#         if contacts.number == loop_counter:
#             ele_class = "active"
#         ele = '''<li class=%s><a href="?page=%s%s">%s</a></li>'''%(ele_class, loop_counter, filters, loop_counter)
#
#         return mark_safe(ele)
#     return ''

@register.simple_tag
def render_filter_ele(filter_field, admin_class, filter_conditions):

    # select_ele = """<select name='%s' class='form-control'><option value=''>-------</option>""" %filter_field
    select_ele = """<select name='{filter_field}' class='form-control'><option value=''>-------</option>"""

    field_obj = admin_class.model._meta.get_field(filter_field)
    # print(field_obj)
    if field_obj.choices:
        selected = ''
        # print(field_obj.choices)
        for choice_item in field_obj.choices:
            if filter_conditions.get(filter_field) == str(choice_item[0]):
                selected = "selected"
            select_ele += '''<option value='%s' %s>%s</option>'''%(choice_item[0], selected, choice_item[1])
            selected = ''
    if type(field_obj).__name__ == "ForeignKey":
        selected = ''
        for choice_item in field_obj.get_choices()[1:]:
            if filter_conditions.get(filter_field) == str(choice_item[0]):
                selected = "selected"
            select_ele += '''<option value='%s' %s>%s</option>'''%(choice_item[0], selected, choice_item[1])
            selected = ''
    if type(field_obj).__name__ in ['DateTimeField', 'DateField']:
        date_els = []
        today_ele = datetime.now().date()
        date_els.append(['今天', datetime.now().date()])
        date_els.append(["昨天", today_ele - timedelta(days=7)])
        date_els.append(["近七天", today_ele - timedelta(days=7)])
        date_els.append(["本月", today_ele.replace(day=1)])
        date_els.append(["近30天", today_ele - timedelta(days=30)])
        date_els.append(["近90天", today_ele - timedelta(days=90)])
        date_els.append(["近180天", today_ele - timedelta(days=180)])
        date_els.append(["本年", today_ele.replace(month=1, day=1)])
        date_els.append(["近一年", today_ele - timedelta(days=365)])

        selected = ''
        for item in date_els:
            select_ele += '''<option value='%s' %s>%s</option>'''%(item[1],selected, item[0])

        filter_field_name = "%s__gte"% filter_field
    else:
        filter_field_name = filter_field
    select_ele += '</select>'
    select_ele = select_ele.format(filter_field=filter_field_name)

    return mark_safe(select_ele)


@register.simple_tag
def build_paginators(contacts, filter_conditions,previous_orderby_page,search_text):
    '''返回整个分页元素'''
    page_btns = ''
    filters = ''
    #添加选中条件的url中的参数
    for k,v in filter_conditions.items():
        filters += "&%s=%s"%(k,v)
    added_dot_ele = False
    for page_num in contacts.paginator.page_range:
        if page_num < 3 or page_num > contacts.paginator.num_pages - 2:
            ele_class = ""
            if contacts.number == page_num:

                ele_class = 'active'
            page_btns += '''<li class=%s><a href="?page=%s%s&o=%s&_q=%s">%s</a></li>'''\
                         %(ele_class, page_num, filters, previous_orderby_page, search_text, page_num)
        elif abs(contacts.number - page_num) <= 1:
            ele_class = ""
            if contacts.number == page_num:
                added_dot_ele = False
                ele_class = "active"
            page_btns += '''<li class=%s><a href="?page=%s%s">%s</a></li>'''\
                         %(ele_class, page_num, filters, page_num)
        else:
            if added_dot_ele == False:
                page_btns += '<li><a>...</a></li'
                added_dot_ele = True
    return mark_safe(page_btns)


@register.simple_tag
def build_table_header_column(column, orderby_key, filter_conditions):

    filters = ''
    # 添加选中条件的url中的参数
    for k, v in filter_conditions.items():
        filters += "&%s=%s" % (k, v)

    ele = '''<th><a href="?{filters}&o={orderby_key}">{column}</a>
    {sort_icon}</th>'''
    if orderby_key:
        if orderby_key.startswith('-'):
            sort_icon = '''<span class="glyphicon glyphicon-chevron-up" aria-hidden="true"></span>'''
        else:
            sort_icon = '''<span class="glyphicon glyphicon-chevron-down" aria-hidden="true"></span>'''

        if orderby_key.strip("-") == column:#要排序的就是这个字段
            orderby_key = orderby_key
        else:
            orderby_key = column
            sort_icon = ''
    else:
        orderby_key = column
        sort_icon = ''
    return  mark_safe(ele.format(filters=filters, orderby_key=orderby_key, column=column, sort_icon=sort_icon))


@register.simple_tag
def get_model_name(admin_class):

    return  admin_class.model._meta.verbose_name

@register.simple_tag
def get_m2m_obj_list(admin_class, field, form_obj):
    '''返回m2m所有待选数据,左边框'''
    field_obj = getattr(admin_class.model, field.name)
    all_obj_list = field_obj.rel.model.objects.all()

    obj_instance_field = getattr(form_obj.instance, field.name)
    selected_obj_list = obj_instance_field.all()

    standby_obj_list = []
    for obj in all_obj_list:
        if obj not in selected_obj_list:
            standby_obj_list.append(obj)

    return standby_obj_list


@register.simple_tag
def get_m2m_selected_obj_list(form_obj, field):
    '''返回已选择的数据，右边框'''
    field_obj = getattr(form_obj.instance, field.name)
    return field_obj.all()
