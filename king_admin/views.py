from django.shortcuts import render,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
from king_admin import king_admin
from king_admin.utils import table_filter, table_sort, table_search
from king_admin.forms import create_model_form

def index(request):
    #一个包含app_name和table_name和admin_class的大字典
    return render(request,"king_admin/table_index.html", {"table_list":king_admin.enabled_admins})


def display_table_objs(request, app_name, table_name):#传进来的CRM_test、userprofile
    # print("-->", app_name, table_name)
    admin_class = king_admin.enabled_admins[app_name][table_name]#根据CRM_test、userprofile取到admin_class

    # contact_list = admin_class.model.objects.all()
    contact_list, filter_conditions = table_filter(request, admin_class)#过滤后的结果

    contact_list = table_search(request, admin_class, contact_list)

    contact_list, orderby_key = table_sort(request, admin_class, contact_list)#排序后的结果
    print(contact_list)
    paginator = Paginator(contact_list, admin_class.list_per_page)  # Show list_per_page contacts per page

    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    # print(admin_class.list_filters)
    return render(request, "king_admin/table_obj.html", {"admin_class": admin_class,
                                                         "contacts": contacts,
                                                         "filter_conditions":filter_conditions,
                                                         "orderby_key":orderby_key,
                                                         "previous_orderby_page":request.GET.get("o", ''),
                                                         "search_text": request.GET.get("_q", '')
                                                         })


def table_obj_change(request, app_name, table_name, obj_id):
    admin_class = king_admin.enabled_admins[app_name][table_name]
    model_form_class = create_model_form(request, admin_class)
    obj = admin_class.model.objects.get(id=obj_id)
    if request.method == "POST":
        form_obj = model_form_class(request.POST, instance=obj)#不加instance=是创建，会报错!加上之后，二者进行对比，有异处开始更新
        if form_obj.is_valid():
            form_obj.save()
    else:#get_method
        form_obj = model_form_class(instance=obj)#表里有数据了

    return render(request, "king_admin/table_obj_change.html", {"form_obj": form_obj,
                                                                "admin_class": admin_class})


def table_obj_add(request, app_name, table_name):

    admin_class = king_admin.enabled_admins[app_name][table_name]
    model_form_class = create_model_form(request, admin_class)

    if request.method == "POST":
        form_obj = model_form_class(request.POST)  #Add
        if form_obj.is_valid():
            form_obj.save()
            return redirect(request.path.replace("/add/", '/'))
    else:  # get-method
        form_obj = model_form_class()  # 表里有数据了

    return render(request, "king_admin/table_obj_add.html", {"form_obj": form_obj})