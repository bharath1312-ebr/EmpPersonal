from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'empviewsets',views.EmpViewset, basename = 'user')

urlpatterns = [
    path('hello/',views.hello_api),
    path('data/',views.get_data),
    path('get_single_data/<id>',views.get_single_data),
    path('change_password/<id>',views.change_password),
    path('cls_data',views.EmpPersonalListView.as_view()),
    path('detail_view/<id>',views.EmpDetailView.as_view()),
    path('generic_list',views.EmpList_Generic.as_view()),
    path('generic_create',views.EmpCreate_Generic.as_view()),
    path('generic_Retrieve/<id>',views.EmpRetrieve_Generic.as_view()),
    path('generic_update/<id>',views.EmpUpdate_Generic.as_view()),
    path('generic_delete/<id>',views.EmpDelete_Generic.as_view()),
    path('generic_list_Create',views.EmpList_Create_Generic.as_view()),
    path('generic_retrieve_update/<name>',views.EmpRetrieve_Update_Generic.as_view()),
    path('generic_retrieve_delete/<name>',views.EmpRetrieve_Delete_Generic.as_view()),
    path('generic_retrieve_delete_update/<name>',views.EmpRetrieve_Delete_Update_Generic.as_view()),
    path('forgot_password',views.user_send_email),
    path('verify_otp',views.verify_otp,name='verify_otp'),
    path('new_password/<id>',views.new_password,name='new_password'),
    path('viewset_list',views.EmpViewset.as_view({'get':'list'}))
]

urlpatterns += router.urls 
