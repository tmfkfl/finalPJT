from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *

from django.core.paginator import Paginator
# Create your views here.
# M(Model) - data

def main(request):
    print(">>>>>DEBUG , client path: /index, main() call, render /board/index.html")

    if request.session.get('session_user_id') :
        print('>>>>>> debug, session exits')
        context = {}
        context['name'] = request.session['session_name']
        context['img'] = request.session['session_img']
        context['user_id'] = request.session['session_user_id']

        return render(request , 'board/main.html',context)
    # else :
    #     print('>>> debug, session not')

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

    #ORM - select * from board_tbl order by id desc;
    #all() - 전체 데이터 검색
    # order_by() - 정렬(- 내림차순)
    boards = board_tbl.objects.all().order_by('-id')
    print(">>>>debug, result , type = ", boards, type(boards))

    paginator = Paginator(boards, 2)
    page = int(request.GET.get('page',1))
    board_list = paginator.get_page(page)



    context = {'boards': board_list }

    # 세션유지를 위해서 다시한번 심는 작업이 필요함.
    context['name'] = request.session['session_name']
    context['img'] = request.session['session_img']
    context['user_id'] = request.session['session_user_id']

    return render(request, 'board/list.html', context)

def joinForm(request):
    print(">>>>>DEBUG , client path: /joinForm, joinForm() call, render /board/join.html")
    return render(request , 'board/join.html')

def join(request):
    print(">>>>>DEBUG , client path: /join, join() call, render /board/join.html")
    id = request.POST['id']
    pwd = request.POST['pwd']
    name = request.POST['name']
    print(">>>>>debug, params id= ", id, "pwd =", pwd, "name =", name)

   # ORM table == class
   # insert into table(cloum) values(id, pwd, name)
   # save() create()
    user_tbl(user_id = id, user_pwd = pwd, user_name = name, user_img = 'boy.png').save()


    return redirect('index')

def registerForm(request):
    print(">>>>>DEBUG , client path: /bbsForm, bbsForm() call, render /board/register.html")

    context = {}

    # 세션을 컨텍스트에 심는 작업

    context['name'] = request.session['session_name']
    context['img'] = request.session['session_img']
    context['user_id'] = request.session['session_user_id']

    # ORM table == class
    # insert into table(cloum) values(id, pwd, name)
    # save() create()
    #board_tbl(title=title, writer=writer,con).save()

    return render(request , 'board/register.html', context)

def register(request):
    print(">>>>>DEBUG , client path: /join, join() call, render /board/join.html")
    title = request.POST['title']
    writer = request.POST['writer']
    content = request.POST['content']
    print(">>>>>debug, params title= ", title, "writer =", writer, "content =", content)

   # ORM table == class
   # insert into table(cloum) values(id, pwd, name)
   # save() create()
    board_tbl(title = title, writer = user_tbl.objects.get(user_id=writer), content = content).save()


    return redirect('list')

#게시르의 식별번호 id를 파라미터로 받아서
#해당 게시글의 정보를 디비에서 select 후
#화면에서 랜더링(read.html)
def read(request):

    id = request.GET.get('id')

    # ORM : select * from board_tbl where id =?
    #boards = board_tbl.objects.all()
    board = board_tbl.objects.get(id=id)
    #print(">>>>debug, result , type = ", board, type(board))
    #ORM : update board_tbl set viewcnt =viewcont +1 where id=?
    board.viewcnt = board.viewcnt +1
    board.save()

    context = {'board': board}

    # 세션유지를 위해서 다시한번 심는 작업이 필요함.
    context['name'] = request.session['session_name']
    context['img'] = request.session['session_img']
    context['user_id'] = request.session['session_user_id']


    return render(request, 'board/read.html', context)

# def delete(request):
#     #print('>>>>Debug')
#     id = request.GET.get('id')
#     # ORM : select * from board_tbl where id =?
#     # boards = board_tbl.objects.all()
#     board = board_tbl.objects.get(id=id)
#     # print(">>>>debug, result , type = ", board, type(board))
#
#     context = {'board': board}
#     board_tbl(id= id).delete()
#
#     # 세션유지를 위해서 다시한번 심는 작업이 필요함.
#     context['name'] = request.session['session_name']
#     context['img'] = request.session['session_img']
#     context['user_id'] = request.session['session_user_id']
#
#     return redirect('list')
def delete(request):
    id = request.GET.get('id')
    board_tbl.objects.get(id=id).delete()
    return redirect('list')
# def update(request):
#
#     id = request.GET.get('id')
#
#     # ORM : select * from board_tbl where id =?
#     #boards = board_tbl.objects.all()
#     board = board_tbl.objects.get(id=id)
#     #print(">>>>debug, result , type = ", board, type(board))
#
#     context = {'board': board}
#
#     # 세션유지를 위해서 다시한번 심는 작업이 필요함.
#     context['name'] = request.session['session_name']
#     context['img'] = request.session['session_img']
#     context['user_id'] = request.session['session_user_id']
#
#
#     return render(request, 'board/update.html', context)
#
def update(request):
   id = request.GET.get('id')
   title = request.GET.get('title')
   content = request.GET.get('content')
   # ORM
   # select * from board_tbl where id =?
   # update board_tbl set title= ? and content =? where=id?
   board =board_tbl.objects.get(id=id)
   board.title = title
   board.content = content
   board.save()
   return redirect('list')

def logout(request):
    request.session['session_name'] = {}
    request.session['session_img'] = {}
    request.session['session_user_id'] ={}

    return redirect('index')

def search(request) :
    print('>>>>>>> debug, client path :/search , search() call(), ajax JsonResponse')
    type = request.POST.get('searchType')
    keyword = request.POST.get('searchKeyword')
    print('debug>>>>>> params', type , keyword)

    # ORM - searchType(title, writer)
    # where title = ?, writer =?
    # like %keyword%, %keyword, keyword%
    # filter( xxxx__icontains, xxxx__endswith, xxxx__startswith)
    if type == 'title' :
         # select * from table where title like '%keyword%'
        boards = board_tbl.objects.filter(title__icontains=keyword)
    elif type == 'writer' :
        # select * from table where writer like '%keyword%'
        boards = board_tbl.objects.filter(writer_id=keyword)

    # QyerySet[<object>,<object> .......]
    print('>>>>debug , result len =', len(boards))
    response_json=[]
    for board in boards :
        response_json.append({
            'id'       : board.id,
            'title'    : board.title,
            'writer'   : board.writer.user_id,
            'regdate'  : board.regdate,
            'viewcnt'  : board.viewcnt

        })
    print('>>>>>>>> json data =', response_json)
    return JsonResponse(response_json, safe=False)