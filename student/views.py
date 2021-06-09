from index.models import Achievement, Student
from django.shortcuts import redirect, HttpResponseRedirect, render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_GET, require_http_methods
from django.contrib.auth.decorators import login_required, permission_required
from .forms import AchievementForm
from django.contrib import messages
from . import extensions


@require_GET
@login_required
@permission_required(['index.student'])
def dashboard(request):
    content = {}
    content.update({"date": extensions.now()})
    return render(request, "student/managing.html", content)


@require_http_methods(["GET", "POST"])
@login_required
@permission_required(['index.student'])
def achievement(request):
    achievement_list = Achievement.objects.filter(is_main=True, 
            owner_id=Student.objects.get(meli_code=request.user.meli_code).id)
    if request.method == 'GET':
        if 'order' in request.GET:
            achievement_list = achievement_list.order_by(request.GET.get('order'))
    elif request.method == 'POST':
        achievement_list = extensions.search_fields(request, achievement_list, 'achievement')
    content = {
        "achievement": achievement_list
    }
    content.update({"date": extensions.now()})
    return render(request, "student/managing.html", content)


@require_http_methods(["GET", "POST"])
@login_required
@permission_required(['index.student'])
def achievement_form(request, refrence_id):
    request.POST._mutable = True
    if request.method == "GET":
        if refrence_id == 0:
            content = {
                "form": AchievementForm()
            }
        else:
            obj = get_object_or_404(
                Achievement, refrence_id=refrence_id, is_main=True)
            initial = {
                "owner": obj.owner, "title": obj.title, "year": obj.year, "field": obj.field, "level": obj.level,
                "dore": obj.dore, "video_link": obj.video_link, "detail": obj.detail, "pic": obj.pic
            }
            content = {
                "form": AchievementForm(initial=initial)
            }
            content.update({"date": extensions.now()})
        return render(request, "student/form.html", content)
    elif request.method == "POST":
        request.POST['owner'] = get_object_or_404(Student, meli_code=request.user.meli_code).id
        request.POST["refrence_id"] = refrence_id
        request.POST["modify_level"] = 'student'
        filled_form = AchievementForm(request.POST, request.FILES)
        if filled_form.is_valid():
            filled_form.save()
            messages.success(
                request, "تغییرات با موفقیت ثبت و پس از تایید مسئول نهایی خواهد شد.")
            return redirect('student:dashboard')
        else:
            messages.error(request, "خطا، اطلاعات وارد شده معتبر نمی باشد.")
            return HttpResponseRedirect(reverse("student:achievement_form",
                                                kwargs={"refrence_id": refrence_id}))

@require_GET
@login_required
@permission_required(['index.student'])
def achievement_delete(request, refrence_id):
    ref_obj = get_object_or_404(
        Achievement, refrence_id=refrence_id, is_main=True)
    new_obj = Achievement(owner=ref_obj.owner, title=ref_obj.title, year=ref_obj.year, field=ref_obj.field,
                          level=ref_obj.level, dore=ref_obj.dore, pic=ref_obj.pic, video_link=ref_obj.video_link,
                          detail=ref_obj.detail)
    new_obj.refrence_id = ref_obj.refrence_id
    new_obj.is_deleted = True
    new_obj.modify_level = 'student'
    new_obj.save()
    messages.success(request, "درخواست با موفقیت ثبت شد")
    return redirect('student:achievement')


@require_GET
@login_required
@permission_required(['index.student'])
def achievement_waiting(request):
    achievement_waiting_list = Achievement.objects.filter(is_main=False,
                                                modify_level__in=['student'], 
                                                owner_id=get_object_or_404(Student, meli_code=request.user.meli_code).id)
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
    return render(request, "student/managing.html", content)


@require_GET
@login_required
@permission_required(['index.student'])
def achievement_confirm_deny(request, action, refrence_id, id):
    obj = get_object_or_404(Achievement, refrence_id=refrence_id, id=id)
    if action == 'deny':
        obj.delete()
        messages.success(request, "درخواست تغییرات رد شد")
    return redirect('student:achievement_waiting')
