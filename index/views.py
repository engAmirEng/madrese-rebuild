from django.shortcuts import render, get_object_or_404
from .models import Student, Achievement
from . import extensions
from django.views.decorators.http import require_http_methods, require_GET


def error_400(request, exception):
        data = {}
        return render(request,'errors/error400.html', data)
def error_403(request, exception):
        data = {}
        return render(request,'errors/error403.html', data)
def error_404(request, exception):
        data = {}
        return render(request,'errors/error404.html', data)
def error_503(request, exception):
        data = {}
        return render(request,'errors/error503  .html', data)


@require_http_methods(['GET', 'POST'])
def index(request):
    achievement_list = Achievement.objects.filter(is_main=True)
    if request.method == 'GET':
        content = {
            'achievement':achievement_list
        }
    elif request.method == "POST":
        content = {
            'achievement':extensions.search_fields(request, achievement_list)
        }
    return render(request, 'index/index_detail.html', content)


@require_GET
def detail(request, refrence_id):
    obj = get_object_or_404(Achievement, refrence_id=refrence_id, is_main=True)
    y, m, d = extensions.gregorian_to_jalali(obj.owner.birthday.year, obj.owner.birthday.month, obj.owner.birthday.day)
    obj.owner.birthday = f'{y}/{m}/{d}'
    content = {
        "achievement":obj
    }
    return render(request, "index/index_detail.html", content)




