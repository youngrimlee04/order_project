from django.contrib.auth import (
    authenticate,
    login as auth_login, #auth_login 안하고 login하니 장고가 밑에 def login 인지
    logout as auth_logout # 불러오는 함수 auth_logout과 지정한 함수이름 def logout 같으면 충돌
)
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect

from client.views import common_login, common_signup
from .forms import PartnerForm, MenuForm
from .models import Menu



URL_LOGIN = '/partner/login/'
#여기서 user는 장고의 request처럼 장고에서 user_pasees_test에서 자동으로 넘겨준 user임
def partner_group_check(user):
    return "partner" in [group.name for group in user.groups.all()]

# Create your views here.
# 장고에서 views.py에서 사용하도록 request라는 파라미터를 자동으로 넘겨주면 받아서 씀
def index(request): #ctx에 담아서 form 넘김
    ctx = {}
    if request.method=="GET":
        partner_form=PartnerForm()
        ctx.update({"form" : partner_form})
    elif request.method=="POST":
        partner_form=PartnerForm(request.POST)
        if partner_form.is_valid():
            partner=partner_form.save(commit=False) # save의 commit은 db에 저장할지 묻는것
            partner.user=request.user
            partner.save()
            return redirect("/partner/")
# 저장 안하는 이유는? model에서는 user있는데 form에서 없기 때문에 user 집어넣어야 해서
        else:
            ctx.update({"form" : partner_form})

    return render(request, "index.html",ctx)

def login(request):
    ctx = {}
    return common_login(request, ctx,"partner")

    # if request.method == "GET":
    #     pass
    # elif request.method == "POST":
    #     username = request.POST.get("username")
    #     password = request.POST.get("password")
    #     user = authenticate(username=username, password=password) #from에 import한 함수를 가져다 써줌
    #     if user is not None:
    #         auth_login(request, user)
    #         next_value = request.GET.get("next") #next로 깃발 꽂기
    #         if next_value:
    #             return redirect(next_value)
    #         else:
    #             return redirect("/partner/") #로그인 후 특정 페이지(파트너라는 메인)로 넘기는 작업
    #     else:
    #         ctx.update({"error":"사용자가 없습니다."})
    #
    # return render(request, "login.html",ctx)

def signup(request):
    ctx = {}
    return common_signup(request,ctx,"partner")

def logout(request):
    auth_logout(request)
    return redirect("/partner/")

@login_required(login_url=URL_LOGIN)
@user_passes_test(partner_group_check, login_url=URL_LOGIN)
def edit_info(request):
    ctx = {}
    # Article.objects.all() 같은 쿼리(DB에 질문 통해 data 가져옴)
    if request.method=="GET":
        partner_form=PartnerForm(instance=request.user.partner)
        ctx.update({"form" : partner_form})
    elif request.method=="POST":
        partner_form=PartnerForm(
            request.POST,
            instance=request.user.partner
        )
        if partner_form.is_valid():
            partner = partner_form.save(commit=False) # save의 commit은 db에 저장할지 묻는것
            partner.user=request.user
            partner.save()
            return redirect("/partner/")
# 저장 안하는 이유는? model에서는 user있는데 form에서 없기 때문에 user 집어넣어야 해서
        else:
            ctx.update({"form" : partner_form})

    return render(request, "edit_info.html",ctx)

@login_required(login_url=URL_LOGIN)
@user_passes_test(partner_group_check, login_url=URL_LOGIN)
def menu(request):
    ctx={}
    # if request.user.is_anonymous or request.user.partner is None:
    #     return redirect("/partner/")
    menu_list = Menu.objects.filter(partner = request.user.partner)
    ctx.update({"menu_list":menu_list}) # 업데이트된 내용을 menu_list.html에서 사용가능
    return render(request, "menu_list.html",ctx)

@login_required(login_url=URL_LOGIN)
@user_passes_test(partner_group_check, login_url=URL_LOGIN)
def menu_add(request):
    ctx={}
    # if "partner" not in request.user.groups.all(): #request,user,group 안의 모든 것 가져옴
    #     return redirect(URL_LOGIN)

    if request.method=="GET":
        form=MenuForm() #MenuForm 활성화시킴
        ctx.update({"form":form}) #form키에 form 불러씀
    elif request.method=="POST":
        form=MenuForm(request.POST, request.FILES) #위와 다르게 파일 함께 저장한다는 의미로 request.FILES
        if form.is_valid():
            menu = form.save(commit=False) #메뉴 인스턴스 생성
            menu.partner = request.user.partner
            menu.save()
            return redirect("/partner/menu/")
        else: #에러시 저장 안하고 에러표시와 함께 처리
            ctx.update({"form":form})

    return render(request, "menu_add.html",ctx)

@login_required(login_url=URL_LOGIN)
@user_passes_test(partner_group_check, login_url=URL_LOGIN)
def menu_detail(request, menu_id):
# id값 알기 때문에 메뉴 넘길 수 있음, get은 item을 1개 가져옴
    menu = Menu.objects.get(id=menu_id) # id가 menu_id인 menu를 가져와서
    ctx = {"menu" : menu}
# get, post 구분 안해도 되니 굳이 ctx.update() 안하고 menu를 위와 같은 방식으로 ctx에 넣어줄 수 있음
    return render(request, "menu_detail.html",ctx)

@login_required(login_url=URL_LOGIN)
@user_passes_test(partner_group_check, login_url=URL_LOGIN)
def menu_edit(request, menu_id):
    ctx = {"replacement":"수정"}
    menu = Menu.objects.get(id=menu_id)
    if request.method=="GET":
        form=MenuForm(instance=menu) #MenuForm 활성화시킴
        ctx.update({"form":form}) #form키에 form 불러씀
    elif request.method=="POST":
        form=MenuForm(request.POST, request.FILES, instance=menu) #위와 다르게 파일 함께 저장한다는 의미로 request.FILES
        if form.is_valid():
            menu = form.save(commit=False) #메뉴 인스턴스 생성
            menu.partner = request.user.partner
            menu.save()
            return redirect("/partner/menu/")
        else: #에러시 저장 안하고 에러표시와 함께 처리
            ctx.update({"form":form})
    return render(request, "menu_add.html",ctx)

@login_required(login_url=URL_LOGIN)
@user_passes_test(partner_group_check, login_url=URL_LOGIN)
def menu_delete(request, menu_id):
    menu = Menu.objects.get(id=menu_id)
    menu.delete()
    return redirect("/partner/menu/") #템플릿 필요 없고 삭제 후 이 페이지로 보냄
