from index.models import Achievement, Student
from django.shortcuts import redirect, HttpResponseRedirect, render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_GET, require_http_methods
from django.contrib.auth.decorators import login_required, permission_required
from .forms import AchievementForm, StudentForm
from django.contrib import messages
from django.contrib.auth.models import Permission
from . import extensions


@require_GET
@login_required
@permission_required(['index.manager'])
def dashboard(request):
    content = {}
    content.update({"date": extensions.now()})
    return render(request, 'manager/managing.html', content)


@require_http_methods(["GET", "POST"])
@login_required
@permission_required(['index.manager'])
def achievement(request):
    achievement_list = Achievement.objects.filter(is_main=True)
    if request.method == 'GET':
        if 'order' in request.GET:
            achievement_list = achievement_list.order_by(request.GET.get('order'))
    elif request.method == 'POST':
        achievement_list = extensions.search_fields(request, achievement_list, 'achievement')
    content = {
        "achievement": achievement_list
    }
    content.update({"date": extensions.now()})
    return render(request, "manager/managing.html", content)


@require_http_methods(["GET", "POST"])
@login_required
@permission_required(['index.manager'])
def student(request):
    student_list = Student.objects.all()
    if request.method == 'GET':
        if 'order' in request.GET:
            student_list = student_list.order_by(request.GET.get('order'))
        for i in range(len(student_list)):
            y, m, d = extensions.gregorian_to_jalali(student_list[i].birthday.year, 
                                                    student_list[i].birthday.month, 
                                                    student_list[i].birthday.day)
            student_list[i].birthday = f'{y}/{m}/{d}'
        content = {
            'student' : student_list
        }
    elif request.method == 'POST':
        content = {
            'student' : extensions.search_fields(request, student_list, 'student')
        }
    content.update({'date': extensions.now()})
    return render(request, 'manager/managing.html', content)


@require_http_methods(["GET", "POST"])
@login_required
@permission_required(['index.manager'])
def achievement_form(request, refrence_id):
    request.POST._mutable = True
    if request.method == "GET":
        if refrence_id == 0:
            content = {
                "form": AchievementForm(),
            }
        else:
            obj = get_object_or_404(
                Achievement, refrence_id=refrence_id, is_main=True)
            initial = {
                "owner": obj.owner, "title": obj.title, "year": obj.year, "field": obj.field, 
                "level": obj.level, "dore": obj.dore, "video_link": obj.video_link, 
                "detail": obj.detail, "pic": obj.pic
            }
            content = {
                "form": AchievementForm(initial=initial)
            }
        content.update({"date": extensions.now()})
        return render(request, "manager/form.html", content)
    elif request.method == "POST":
        request.POST["refrence_id"] = refrence_id
        request.POST["modify_level"] = request.user.groups.all()[0].name
        filled_form = AchievementForm(request.POST, request.FILES)
        if filled_form.is_valid():
            filled_form.save()
            messages.success(
                request, "تغییرات با موفقیت ثبت و پس از تایید مسئول نهایی خواهد شد.")
            return redirect('manager:dashboard')
        else:
            messages.error(request, "خطا، اطلاعات وارد شده معتبر نمی باشد.")
            return HttpResponseRedirect(reverse("manager:achievement_form",
                                                kwargs={"refrence_id": refrence_id}))

@require_http_methods(["GET", "POST"])
@login_required
@permission_required(['index.manager'])
def student_form(request, refrence_id):
    request.POST._mutable = True
    if request.method == "GET":
        if refrence_id == 0:
            content = {
                "form": StudentForm(),
            }
        else:
            obj = get_object_or_404(
                Student, id = refrence_id)
            initial = {
                "first_name":obj.first_name, "last_name":obj.last_name, "birthday":obj.birthday, 
                "photo":obj.photo, "meli_code":obj.meli_code
            }
            content = {
                "form":StudentForm(initial=initial)
            }
        content.update({"date": extensions.now()})
        return render(request, "manager/form.html", content)
    elif request.method == "POST":
        jy, jm, jd = request.POST["birthday"].split("/")
        miladi_y, miladi_m, miladi_d = extensions.jalali_to_gregorian(int(jy), int(jm) ,int(jd))
        request.POST["birthday"] = f"{miladi_y}-{miladi_m}-{miladi_d}"
        filled_form = StudentForm(request.POST, request.FILES, instance=get_object_or_404(Student, id=id)) if \
            refrence_id != 0 else StudentForm(request.POST, request.FILES)
        if filled_form.is_valid():
            filled_form.save()
            messages.success(
                request, "تغییرات با موفقیت ثبت شد.")
            return redirect('manager:dashboard')
        else:
            messages.error(request, "خطا، اطلاعات وارد شده معتبر نمی باشد.")
            return HttpResponseRedirect(reverse("manager:student_form",
                                                kwargs={"refrence_id": refrence_id}))


@login_required
@require_GET
@permission_required(['index.manager'])
def achievement_delete(request, refrence_id):
    ref_obj = get_object_or_404(
        Achievement, refrence_id=refrence_id, is_main=True)
    new_obj = Achievement(owner=ref_obj.owner, title=ref_obj.title, year=ref_obj.year, field=ref_obj.field,
                          level=ref_obj.level, dore=ref_obj.dore, pic=ref_obj.pic, video_link=ref_obj.video_link,
                          detail=ref_obj.detail)
    new_obj.refrence_id = ref_obj.refrence_id
    new_obj.is_deleted = True
    new_obj.modify_level = request.user.groups.all()[0].name
    new_obj.save()
    messages.success(
        request, "درخواست با موفقیت ثبت شد و پس ااز تایید نهایی میشود")
    return redirect('manager:achievement')


@login_required
@require_GET
@permission_required(['index.manager'])
def student_delete(request, refrence_id):
    obj = get_object_or_404(Student, id=refrence_id)
    obj.delete()
    messages.success(
        request, "درخواست حذف با موفقیت انجام شد")
    return redirect('manager:student')


@login_required
@require_GET
@permission_required(['index.manager'])
def achievement_waiting(request):
    achievement_waiting_list = Achievement.objects.filter(is_main=False,
                                                modify_level__in=['mentor', 'manager'])
    if 'order' in request.GET:
        if request.GET.get('order') == 'kind':
            achievement_waiting_list = achievement_waiting_list.order_by('refrence_id', 'is_deleted')
        elif request.GET.get('order') == '-kind':
            achievement_waiting_list = achievement_waiting_list.order_by('is_deleted', '-refrence_id')
        else:
            achievement_waiting_list = achievement_waiting_list.order_by(request.GET.get('order'))
    content = {
        "achievement": achievement_waiting_list}
    content.update({"date": extensions.now()})
    return render(request, "manager/managing.html", content)


@login_required
@require_GET
@permission_required(['index.manager'])
def achievement_confirm_deny(request, action, refrence_id, id):
    obj = get_object_or_404(Achievement, refrence_id=refrence_id, id=id)
    if action == 'confirm':
        if refrence_id == 0:
            obj.modify_level = request.user.groups.all()[0].name
            obj.is_main = True if request.user.groups.all()[
                0].name == "manager" else False
            obj.refrence_id = obj.id if request.user.groups.all()[
                0].name == "manager" else 0
            obj.save()
        elif not obj.is_deleted:
            main_obj = get_object_or_404(
                Achievement, refrence_id=refrence_id, is_main=True)
            obj.modify_level = request.user.groups.all()[0].name
            obj.is_main = True if request.user.groups.all()[
                0].name == "manager" else False
            obj.save()
            main_obj.is_main = False if request.user.groups.all()[
                0].name == "manager" else True
            main_obj.save()
            messages.success(request, "با موفقیت اعمال شد")
            if request.user.groups.all()[0].name == "manager":
                main_obj.delete()
                messages.success(request, "با موفقیت جایگزین شد")
        elif obj.is_deleted:
            main_obj = get_object_or_404(
                Achievement, refrence_id=refrence_id, is_main=True)
            obj.delete()
            main_obj.delete()
            messages.success(request, "با موفقیت اعمال شد")
    elif action == "deny":
        obj.delete()
        messages.success(request, "درخواست تغییرات رد شد")
    return redirect('manager:achievement_waiting')
