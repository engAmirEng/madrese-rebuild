from index.models import Achievement
from django.shortcuts import redirect, HttpResponseRedirect, render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_GET, require_http_methods
from django.contrib.auth.decorators import login_required, permission_required
from .forms import AchievementForm
from django.contrib import messages
from django.contrib.auth.models import Permission
from . import extensions


def mentor_specialty(request):
    special_perm = Permission.objects.filter(user=request.user)[0].name
    specialty = None
    if 'parvareshi' in special_perm:
        specialty = 'پرورشی'
    elif 'pazhooheshi' in special_perm:
        specialty = 'پژوهشی'
    elif 'varzeshi' in special_perm:
        specialty = 'ورزشی'
    elif 'amoozeshi' in special_perm:
        specialty = 'آموزشی'
    return specialty


@require_GET
@login_required
@permission_required(['index.mentor'])
def dashboard(request):
    content = {}
    content.update({"date": extensions.now()})
    return render(request, 'mentor/managing.html', content)


@require_http_methods(["GET", "POST"])
@login_required
@permission_required(['index.mentor'])
def achievement(request):
    field = mentor_specialty(request)
    achievement_list = Achievement.objects.filter(is_main=True, field=field)
    if request.method == 'GET':
        if 'order' in request.GET:
            achievement_list = achievement_list.order_by(request.GET.get('order'))
    elif request.method == 'POST':
        achievement_list = extensions.search_fields(request, achievement_list)
    content = {
    "achievement": achievement_list
    }
    content.update({"date": extensions.now()})
    return render(request, "mentor/managing.html", content)


@require_http_methods(["GET", "POST"])
@login_required
@permission_required(['index.mentor'])
def achievement_form(request, refrence_id):
    request.POST._mutable = True
    mentor = mentor_specialty(request)
    if request.method == "GET":
        if refrence_id == 0:
            content = {
                "form": AchievementForm(),
                'mentor': mentor
            }
        else:
            obj = get_object_or_404(
                Achievement, refrence_id=refrence_id, is_main=True,
                field=mentor_specialty(request)
            )
            initial = {
                "owner": obj.owner, "title": obj.title, "year": obj.year,
                "field": obj.field, "level": obj.level, "dore": obj.dore,
                "video_link": obj.video_link, "detail": obj.detail, "pic": obj.pic
            }
            content = {
                "form": AchievementForm(initial=initial)
            }
        content.update({"date": extensions.now()})
        return render(request, "mentor/form.html", content)
    elif request.method == "POST":
        request.POST["refrence_id"] = refrence_id
        request.POST["modify_level"] = request.user.groups.all()[0].name
        request.POST['field'] = mentor
        filled_form = AchievementForm(request.POST, request.FILES)
        if filled_form.is_valid():
            filled_form.save()
            messages.success(
                request, "تغییرات با موفقیت ثبت و پس از تایید مسئول نهایی خواهد شد.")
            return redirect('mentor:dashboard')
        else:
            messages.error(request, "خطا، اطلاعات وارد شده معتبر نمی باشد.")
            return HttpResponseRedirect(reverse("mentor:achievement_form",
                                                kwargs={"refrence_id": refrence_id}))


@login_required
@require_GET
@permission_required(['index.mentor'])
def achievement_delete(request, refrence_id):
    ref_obj = get_object_or_404(
        Achievement, refrence_id=refrence_id, is_main=True, field=mentor_specialty(request)
    )
    new_obj = Achievement(owner=ref_obj.owner, title=ref_obj.title, year=ref_obj.year, field=ref_obj.field,
                          level=ref_obj.level, dore=ref_obj.dore, pic=ref_obj.pic, video_link=ref_obj.video_link,
                          detail=ref_obj.detail)
    new_obj.refrence_id = ref_obj.refrence_id
    new_obj.is_deleted = True
    new_obj.modify_level = request.user.groups.all()[0].name
    new_obj.save()
    messages.success(request, "درخواست با موفقیت ثبت شد")
    return redirect('mentor:achievement')


def achievement_waiting(request):
    achievement_waiting_list = Achievement.objects.filter(is_main=False,
                                                modify_level__in=[
                                                    'student', 'mentor'],
                                                field=mentor_specialty(request))
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
    return render(request, "mentor/managing.html", content)


def achievement_confirm_deny(request, action, refrence_id, id):
    obj = get_object_or_404(
        Achievement, refrence_id=refrence_id, id=id, field=mentor_specialty(request))
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
    return redirect('mentor:achievement_waiting')
