from typing import get_args
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.views.decorators.http import require_POST, require_http_methods
from index.models import Student
#sensitive infos are stored in secValues
import secValues

User = get_user_model()    #it's because we defines our custom user model

# validating registery form
def reg_validation(request):
    status = True
    if User.objects.filter(username=request.POST["username"]).exists():
        messages.error(request, "نام کاربری وارد شده قبلا انخاب شده است!")
        status = False
    if User.objects.filter(email=request.POST["email"]).exists():
        messages.error(request, "این ایمیل در سیستم موجود است!")
        status = False
    if request.POST["password"] != request.POST["confirm_password"]:
        messages.error(request, "رمز های عبور وارد شده یکسان نیستند!")
        status = False
    if 'student' in request.path:
        if not Student.objects.filter(meli_code = request.POST['meli_code']).exists():
            messages.error(request, 'کد ملی شما در سیستم ثبت نشده است')
            status = False
        elif Student.objects.get(meli_code=request.POST['meli_code']).first_name != request.POST['first_name'] \
        or Student.objects.get(meli_code=request.POST['meli_code']).last_name != request.POST['last_name']:
            messages.error(request, 'اطلاعات وارد شده با اطلاعات موجود در سیستم همخوانی ندارد')
            status = False
    return status

# validating registery form
def login_validation(request, user):
    if user is not None:
        status = True
        messages.success(request, "وارد شدید")
    elif User.objects.filter(username=request.POST["username"]).exists() and \
        User.objects.get(username=request.POST['username']).is_active:
        messages.error(request, "رمز عبور را صحیح وارد کنید")
        status = False
    elif User.objects.filter(username=request.POST["username"]).exists() and \
        not User.objects.get(username=request.POST['username']).is_active:
        messages.error(request, "دسترسی شما توسط مسئول مربوطه تایید نشده است")
        status = False
    else:
        messages.error(request, "نام کاربری وارد شده ثبت نشده است")
        status = False
    return status

# login
@require_http_methods(['GET', 'POST'])
def login(request):
    salt = secValues.salt
    if request.method == "POST":
        user = auth.authenticate(username=request.POST["username"], password=request.POST["password"]+salt)
        status = login_validation(request, user)
        if status:
            auth.login(request, user)
            if request.user.has_perm('index.student'):
                return redirect('student:dashboard')
            elif request.user.has_perm('index.mentor'):
                return redirect('mentor:dashboard')
            elif request.user.has_perm('index.manager'):
                return redirect('manager:dashboard')
        return redirect("accounts:login")
    elif request.method == "GET":
        return render(request, "accounts/login.html")

# register students
@require_http_methods(['GET', 'POST'])
def register_student(request):
    salt = secValues.salt
    if request.method == "POST":
        status = reg_validation(request)
        if status:
            user = User.objects.create_user(first_name=request.POST["first_name"], 
                                            last_name=request.POST["last_name"], 
                                            username=request.POST["username"], 
                                            password=request.POST["password"]+salt, 
                                            meli_code=request.POST['meli_code'], 
                                            email=request.POST["email"], 
                                            is_active=False)
            user.save()
            user.groups.add(Group.objects.get(name='student').id)
            messages.success(request, 'ثبت نام شما با موفقیت ثبت شد، پس از تایید مدیر سیستم میتوانید وارد شوید')
            return redirect("index:index")
        return redirect("accounts:register_student")
    elif request.method == "GET":
        return render(request, "accounts/register.html")

# register mentors
@require_http_methods(['GET', 'POST'])
def register_mentor(request):
    salt = secValues.salt
    if request.method == "POST":
        status = reg_validation(request)
        if status:
            user = User.objects.create_user(first_name=request.POST["first_name"], 
                                            last_name=request.POST["last_name"], username=request.POST["username"], 
                                            password=request.POST["password"]+salt, 
                                            email=request.POST["email"], is_active=False)
            user.save()
            user.groups.add(Group.objects.get(name='mentor').id)
            user.user_permissions.add(Permission.objects.get(codename=request.POST["field_of_mentoring"]).id)
            messages.success(request, 'ثبت نام شما با موفقیت ثبت شد، پس از تایید مدیر سیستم میتوانید وارد شوید')
            return redirect("index:index")
        return redirect("accounts:register_mentor")
    elif request.method == "GET":
        return render(request, "accounts/register.html")

# register managers
@require_http_methods(['GET', 'POST'])
def register_manager(request):
    salt = secValues.salt
    if request.method == "POST":
        status = reg_validation(request)
        if status:
            user = User.objects.create_user(first_name=request.POST["first_name"], 
                                            last_name=request.POST["last_name"], username=request.POST["username"], 
                                            password=request.POST["password"]+salt, 
                                            email=request.POST["email"], is_active=False)
            user.save()
            user.groups.add(Group.objects.get(name='manager').id)
            messages.success(request, 'ثبت نام شما با موفقیت ثبت شد، پس از تایید مدیر سیستم میتوانید وارد شوید')
            return redirect("index:index")
        return redirect("accounts:register_manager")    
    elif request.method == "GET":
        return render(request, "accounts/register.html")

@require_POST
def logout(request):
    auth.logout(request)
    messages.info(request, "با موفقیت خارج شدید")
    return redirect("index:index")