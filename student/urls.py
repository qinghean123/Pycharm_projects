

from django.urls import path
from student import views

urlpatterns = [

    path('index/', views.index, name="sales_index"),

    path('students/', views.student_list, name="stu_index"),

]
