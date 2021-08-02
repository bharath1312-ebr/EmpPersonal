from django.urls import path
from .views import user_register , basic_load , user_modelform, user_form, html_form, get_userlist, single_data , update_data, delete_user, user_login, user_logout, forgot_password, verify_otp, changing_password
from .views import Hello_sample, EmpPer_cls, EmpPer_List, EmpPer_Update, EmpPer_Delete, EmpPer_Detail

urlpatterns = [
    path('user_register',user_register, name='user_register'),
    path('basic/',basic_load, name='basic_load'),
    path('modelform/',user_modelform, name='user_modelform'),
    path('normalform/',user_form, name='user_form'),
    path('html_form/',html_form, name='html_form'),
    path('',get_userlist, name='get_userlist'),
    path('get_single/<id>',single_data, name='single_data'),
    path('update/<id>',update_data, name='update_data'),
    path('deleteuser/<id>',delete_user, name='delete_user'),
    path('login/', user_login, name='user_login'),
    path('logout/',user_logout, name='user_logout'),
    path('forgotpassword/',forgot_password,name='forgot_password'),
    path('verifyingotp/',verify_otp,name = 'verify_otp'),
    path('newpassword/<id>',changing_password, name='changing_password'),
    path('hello_cls',Hello_sample.as_view(), name='hello_cls'),
    path('empper_cls',EmpPer_cls.as_view(), name="empper_cls"),
    path('empper_List/',EmpPer_List.as_view(), name="empper_List"),
    path('empper_Update/<pk>',EmpPer_Update.as_view(), name="empper_Update"),
    path('empper_Delete/<pk>',EmpPer_Delete.as_view(), name="empper_Delete"),
    path('empper_Detail/<pk>',EmpPer_Detail.as_view(), name="empper_Detail")

]