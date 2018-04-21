from django.db.models import Q

def table_filter(request, admin_class):
    '''进行条件过滤，并返回数据'''
    filter_conditions = {}
    key_words = ['page', 'o', '_q']
    for k,v in request.GET.items():

        if k in key_words:#保留关键字分页和排序关键字段
            continue
        # print('k=%s ; v=%s'%(k,v))
        if v:
            filter_conditions[k] = v
    # print(filter_conditions)

    return admin_class.model.objects.filter(**filter_conditions).\
                order_by("-%s" %admin_class.ordering if admin_class.ordering else "-id"), filter_conditions

def table_sort(request, admin_class, objs):
    orderby_key = request.GET.get("o")
    print('orderby_key:',orderby_key)
    if orderby_key:
        res = objs.order_by(orderby_key)#排序后的字段
        if orderby_key.startswith('-'):
            orderby_key = orderby_key.strip('-')
        else:
            orderby_key = "-%s"%orderby_key
    else:
        res = objs
    return res, orderby_key


def table_search(request, admin_class, contact_list):
    search_key = request.GET.get('_q', '')
    q_obj = Q()
    q_obj.connector = "OR"
    for column in admin_class.search_fields:
        q_obj.children.append(("%s__contains"%column, search_key))
    print('hello', q_obj.children)
    res = contact_list.filter(q_obj)
    return res




