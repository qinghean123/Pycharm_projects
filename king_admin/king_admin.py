from CRM_test import models



class BaseAdmin(object):
    list_display = []
    list_filters = []
    search_fields = []
    list_per_page = 20
    ordering = None
    filter_horizontal = []

class CustomerAdmin(BaseAdmin):
    list_display = ['id', 'qq', 'name', 'source', 'consultant', 'consult_course', 'date', 'status']
    list_filters = ['source', 'consultant', 'consult_course', 'status', 'date']
    search_fields = ['qq', 'name', 'consultant__name']
    list_per_page = 5
    ordering = "id"
    filter_horizontal = ('tags',)
class CustomerFollowUpAdming(BaseAdmin):
    list_display = ['customer', 'consultant', 'date']


enabled_admins = {}
def register(model_class, admin_class=None):
    #models.UserProfile._meta.app_label--->CRM_test
    if model_class._meta.app_label not in enabled_admins:
        #{'CRM_test':{}}
        enabled_admins[model_class._meta.app_label] = {}
    #绑定model对象和admin对象
    admin_class.model = model_class
    #{'CRM_test':{'model_name':{}}
    enabled_admins[model_class._meta.app_label][model_class._meta.model_name] = admin_class

register(models.Customer, CustomerAdmin)
register(models.CustomerFollowUp, CustomerFollowUpAdming)

# print(enabled_admins)