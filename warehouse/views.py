from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Goods


# 1. 登录页面
def user_login(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        pwd = request.POST.get('pwd')
        user = authenticate(username=staff_id, password=pwd)
        if user:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'warehouse/login.html', {'err': '工号或密码错误'})
    return render(request, 'warehouse/login.html')


# 2. 退出登录
def user_logout(request):
    logout(request)
    return redirect('user_login')


# 3. 仓库首页（权限区分）
@login_required(login_url='user_login')
def index(request):
    goods_list = Goods.objects.all()
    is_admin = request.user.is_superuser  # 只有超级管理员才为True
    return render(request, 'warehouse/index.html', locals())


# ========== 仅管理员可见：员工管理功能 ==========
@login_required(login_url='user_login')
def staff_manage(request):
    # 普通员工直接拦截，跳回首页
    if not request.user.is_superuser:
        return redirect('index')
    staff_list = User.objects.all()
    return render(request, 'warehouse/staff_manage.html', locals())


# 添加员工
@login_required(login_url='user_login')
def add_staff(request):
    if not request.user.is_superuser:
        return redirect('index')
    if request.method == 'POST':
        sid = request.POST.get('sid')
        pwd = request.POST.get('pwd')
        name = request.POST.get('name')
        # 校验6位纯数字工号
        if len(sid) != 6 or not sid.isdigit():
            return render(request, 'warehouse/add_staff.html', {'msg': '工号必须是6位纯数字'})
        if User.objects.filter(username=sid).exists():
            return render(request, 'warehouse/add_staff.html', {'msg': '该工号已存在'})
        # 创建用户（密码自动哈希加密）
        User.objects.create_user(username=sid, password=pwd, first_name=name)
        return redirect('staff_manage')
    return render(request, 'warehouse/add_staff.html')


# 删除员工
@login_required(login_url='user_login')
def del_staff(request, uid):
    if not request.user.is_superuser:
        return redirect('index')
    User.objects.filter(id=uid).delete()
    return redirect('staff_manage')


# 修改员工密码
@login_required(login_url='user_login')
def edit_pwd(request, uid):
    if not request.user.is_superuser:
        return redirect('index')
    if request.method == 'POST':
        new_pwd = request.POST.get('new_pwd')
        user = User.objects.get(id=uid)
        user.set_password(new_pwd)
        user.save()
        return redirect('staff_manage')
    return render(request, 'warehouse/edit_pwd.html')

# 仓库首页，显示所有商品
@login_required(login_url='user_login')
def index(request):
    goods_list = Goods.objects.all()
    is_admin = request.user.is_superuser
    return render(request, 'warehouse/index.html', {'goods_list': goods_list})

# 商品入库
@login_required(login_url='user_login')
def stock_in(request):
    if request.method == 'POST':
        gid = request.POST.get('gid')
        name = request.POST.get('name')
        num = int(request.POST.get('num'))
        price = float(request.POST.get('price'))

        if Goods.objects.filter(gid=gid).exists():
            # 商品已存在，增加库存
            goods = Goods.objects.get(gid=gid)
            goods.stock += num
            goods.save()
        else:
            # 新增商品
            Goods.objects.create(gid=gid, name=name, stock=num, price=price)
    return redirect('/')

# 商品出库
@login_required(login_url='user_login')
def stock_out(request):
    if request.method == 'POST':
        gid = request.POST.get('gid')
        out_num = int(request.POST.get('out_num'))
        goods = Goods.objects.get(gid=gid)

        if goods.stock >= out_num:
            goods.stock -= out_num
            goods.save()
    return redirect('/')

@login_required(login_url='user_login')
def delete_goods(request, gid):
    # 只允许 POST 请求执行删除，防止恶意 GET 请求
    if request.method == 'POST':
        goods = Goods.objects.filter(gid=gid)
        if goods.exists():
            goods.delete()
            # 删除成功，跳转到商品列表页（如果你的商品列表路由不是 '/'，就改成对应的路径）
            return redirect('goods_list')
        else:
            # 商品不存在，跳转到列表页并提示
            return redirect('goods_list')
    # 不允许 GET 请求，直接返回 405 或跳转
    return redirect('goods_list')