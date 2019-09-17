from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import auth
from blog.untils import validcode
from cnblong.MyForm import UserForm
from .models import UserInfo, Article

# Create your views here.

def login(request):
    if request.method == "POST":
        response = {"user": None, "msg": None}
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        valid_code = request.POST.get("valid_code")
        # 先校验验证码
        if valid_code.upper() == request.session.get("valid_code_str").upper():
            user = auth.authenticate(username=user, password=pwd)
            if user:
                auth.login(request, user)  # request.user == '当前登陆对象'
                response['user'] = user.username
                return JsonResponse(response)
            else:
                response["msg"] = "用户名或者密码错误!"
        else:
            response['msg'] = '验证码错误'
        return JsonResponse(response)

    return render(request, 'login.html')


def get_validcode_img(request):
    data = validcode.validcode(request)
    return HttpResponse(data)


def index(request):
    # auth.logout(request)
    article_list = Article.objects.all()
    return render(request, 'index.html', locals())


def register(request):
    if request.is_ajax():
        print("ajax")
        response = {"user": None, "msg": None}
        form = UserForm(request.POST)
        if form.is_valid():
            response['user'] = form.cleaned_data.get('user')
            user = form.cleaned_data.get("user")
            pwd = form.cleaned_data.get("pwd")
            email = form.cleaned_data.get("email")
            avatar_obj = request.FILES.get("avatar")

            extra = {}
            if avatar_obj:
                extra["avatar"] = avatar_obj

            UserInfo.objects.create_user(username=user, password=pwd, email=email, **extra)
            # 密码进行摘要转换，不能使用create
        else:
            print(form.cleaned_data)
            print(form.errors)
            response['msg'] = form.errors
        return JsonResponse(response)

    form = UserForm()
    return render(request, 'register.html', {'form': form})


def logout(request):
    auth.logout(request)  # 等同于  request.session.flush
    return HttpResponseRedirect(reverse('login'))


def home_site(request, username):
    user = UserInfo.objects.filter(username=username).first()
    # 判断用户是否存在!
    if not user:
        return render(request, "not_found.html")

    # 查询当前站点对象

    blog = user.blog

    # 1 当前用户或者当前站点对应所有文章
    # 基于对象查询
    # article_list=user.article_set.all()
    # 基于 __

    article_list = models.Article.objects.filter(user=user)

    if kwargs:
        condition = kwargs.get("condition")
        param = kwargs.get("param")  # 2012-12

        if condition == "category":
            article_list = article_list.filter(category__title=param)
        elif condition == "tag":
            article_list = article_list.filter(tags__title=param)
        else:
            year, month = param.split("/")
            article_list = article_list.filter(create_time__year=year, create_time__month=month)

    # 每一个后的表模型.objects.values("pk").annotate(聚合函数(关联表__统计字段)).values("表模型的所有字段以及统计字段")

    # 查询每一个分类名称以及对应的文章数

    # ret=models.Category.objects.values("pk").annotate(c=Count("article__title")).values("title","c")
    # print(ret)

    # 查询当前站点的每一个分类名称以及对应的文章数

    # cate_list=models.Category.objects.filter(blog=blog).values("pk").annotate(c=Count("article__title")).values_list("title","c")
    # print(cate_list)

    # 查询当前站点的每一个标签名称以及对应的文章数

    # tag_list=models.Tag.objects.filter(blog=blog).values("pk").annotate(c=Count("article")).values_list("title","c")
    # print(tag_list)

    # 查询当前站点每一个年月的名称以及对应的文章数

    # ret=models.Article.objects.extra(select={"is_recent":"create_time > '2018-09-05'"}).values("title","is_recent")
    # print(ret)

    # 方式1:
    # date_list=models.Article.objects.filter(user=user).extra(select={"y_m_date":"date_format(create_time,'%%Y/%%m')"}).values("y_m_date").annotate(c=Count("nid")).values_list("y_m_date","c")
    # print(date_list)

    # 方式2:

    # from django.db.models.functions import TruncMonth
    #
    # ret=models.Article.objects.filter(user=user).annotate(month=TruncMonth("create_time")).values("month").annotate(c=Count("nid")).values_list("month","c")
    # print("ret----->",ret)
        return render(request, "home_site.html", {"username": username, "blog": blog, "article_list": article_list, })


def test(request):
    from collections import OrderedDict  # 用于保存路由
    from django.urls import URLPattern, URLResolver
    from django.conf import settings
    from django.utils.module_loading import import_string  # 帮助我们以字符串的形式导入模块
    port = import_string(settings.ROOT_URLCONF)
    for k in port.urlpatterns:
        if isinstance(k, URLResolver):  # 路由分发
            print('00000', k, k.namespace)
        elif isinstance(k, URLPattern):  # 非路由分发
            if k.name:
                print('1111', k, k.pattern)
            else:
                print('2222', k, k.pattern)


    return HttpResponse("ok")
