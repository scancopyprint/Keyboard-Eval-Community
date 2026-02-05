from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import Evaluator  # 确保导入您的模型

def tologinpage(request):
 return render(request, 'login.html')
def toregisterpage(request):
 return render(request, 'register.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        # 检查用户名是否存在
        if Evaluator.objects.filter(username=username).exists():
            info = '用户已存在'
        # 检查两次密码是否一致
        elif password != password2:
            info = '两次密码输入不一致'
        else:
            # 创建用户并保存（手动处理密码加密）
            evaluator = Evaluator(username=username)
            evaluator.set_password(password)  # 调用模型中的加密方法
            evaluator.save()
            info = '注册成功，请重新登录'
            logout(request)  # 确保用户未登录
            return redirect('login')  # 假设存在名为'login'的路由

    # locals()会将局部变量传递给模板（包含info）
    return render(request, 'users/register.html', locals())


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        # 检查用户是否存在
        if Evaluator.objects.filter(username=username).exists():
            evaluator = Evaluator.objects.get(username=username)
            # 手动验证密码
            if evaluator.check_password(password):
                # 登录成功：将用户ID存入Session
                request.session['evaluator_id'] = evaluator.id
                return redirect('dashboard')  # 假设存在名为'dashboard'的路由
            else:
                errorinfo = '用户名或密码错误！'
        else:
            errorinfo = '用户不存在，请注册'

    # 渲染模板并传递错误信息
    return render(request, 'users/login.html', locals())