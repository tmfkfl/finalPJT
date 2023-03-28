from django.shortcuts import render

from .models import *
# Create your views here.
# M(Model) - data

def main(request):
    print(">>>>>DEBUG , client path: /index, main() call, render /board/index.html")
    return render(request , 'board/index.html')

def login(request):
    print(">>>>>DEBUG , client path: /login, login() call, render /board/main.html")
    # 사용자의 요청 방식이 GET | POST 에 따라서 달라짐.
    # request.method == 'GET' | request.method == 'POST'
    id = request.POST['id']
    pwd = request.POST['pwd']
    print(">>>>>debug, params id= ", id, "pwd =", pwd)
    #SQL : select * from table where id =id and pwd= pwd;
    #ORM(Object Relational Mapping)
    #table(row) == class(instance)
    # return render(request , 'board/index.html')

    user = user_tbl.objects.get(user_id = id, user_pwd = pwd)
    print('>>>> debug, result = ', user)

    #데이터를 심는 작업
    # dict 형식으로
    #세션생성
    request.session['session_name'] = user.user_name
    request.session['session_img'] = user.user_img
    request.session['session_user_id'] = user.user_id
    # 세션을 컨텍스트에 심는 작업
    context = {}
    context['name']    = request.session['session_name']
    context['img']     = request.session['session_img']
    context['user_id'] = request.session['session_user_id']

    return render(request,'board/main.html', context)

# board : 게시물 목록을 화면에 출려할 수 있도록 데이터베이스로부터 데이터를 가져와 심고 화면을 분기시킨다.
def list(request):
    print(">>>>>DEBUG , client path: /list, list() call, render /board/.html")

    #ORM - select * from board_tbl;
    #all() - 전체 데이터 검색
    boards = board_tbl.objects.all()
    print(">>>>debug, result , type = ", boards, type(boards))

    context = {'boards': boards }

    # 세션유지를 위해서 다시한번 심는 작업이 필요함.
    context['name'] = request.session['session_name']
    context['img'] = request.session['session_img']
    context['user_id'] = request.session['session_user_id']

    return render(request, 'board/list.html', context)