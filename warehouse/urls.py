from django.urls import path
from . import views

urlpatterns = [
    # 登录/登出
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    # 仓库首页
    path('', views.index, name='index'),
    # 商品操作
    path('in/', views.stock_in, name='stock_in'),
    path('out/', views.stock_out, name='stock_out'),
    path('del/<str:gid>/', views.delete_goods, name='delete_goods'),
    # 管理员员工管理
    path('staff/manage/', views.staff_manage, name='staff_manage'),
    path('staff/add/', views.add_staff, name='add_staff'),
    path('staff/del/<int:uid>/', views.del_staff, name='del_staff'),
    path('staff/edit/<int:uid>/', views.edit_pwd, name='edit_pwd'),
]