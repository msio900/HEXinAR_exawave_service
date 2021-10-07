import json

from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
from analysis.keywordissuemap import keywordissuemap_KIM, keywordissuemap_KEM, similarity_word
from frame.clientdb import ClientDB
from frame.error import ErrorCode


def index(request):
    return render(request, 'index.html')

def login_two(request):
    return render(request, 'login_two.html')
def loginimpl(request):
    email = request.POST['email']
    pwd = request.POST['pwd']
    try:
        client = ClientDB().selectOne(pwd, email)
        if pwd == client.getPwd():
            request.session['logininfo'] = {'id': client.getId(), 'name': client.getName(), 'pwd': client.getPwd(),
                                            'email': client.getEmail()}
            return redirect('index')
        else:
            raise Exception
    except:
        context = {'msg': ErrorCode.e02}
        return render(request,'login_two.html' , context)

def logout(request):
    if request.session['logininfo'] != None:
        del request.session['logininfo']
    return redirect('index')

def forget_password(request):
    return render(request, 'forget-password.html')
def sign_up(request):
    return render(request, 'sign-up.html')
def sign_up_one(request):
    return render(request, 'sign-up-one.html')
def sign_up_two(request):
    return render(request, 'sign-up-two.html')
def signupimpl(request):
    try:
        email = request.POST['email']
        pwd = request.POST['pwd']
        name = request.POST['name']
        phone_num = request.POST['phone_num']
        ClientDB().insert(pwd, name, email, phone_num)
        return render(request, 'login_two.html')
    except Exception as err:
        print(err)
        context = {'msg': ErrorCode.e03}
        return render(request, 'sign-up.html', context)

def search(request):
    return render(request, 'search.html')

def search2(request):
    return render(request, 'search2.html')

def general_widget(request):
    return render(request, 'general-widget.html')

def update(request):
    pwd = request.session['logininfo']['pwd']
    email = request.session['logininfo']['email']
    client = ClientDB().selectOne(pwd, email)
    context = {'client': client}
    return render(request, 'update.html', context)
def infoupdate(request):
    try:
        email = request.POST['email']
        pwd = request.POST['pwd']
        name = request.POST['name']
        phone_num = request.POST['phone_num']
        ClientDB().update(pwd, name, phone_num, email)
        return redirect('index')
    except Exception as err:
        print('에러:', err)
        context= {'msg': ErrorCode.e03}
        return render(request, 'update.html', context)

def introduce(request):
    return render(request, 'introduce.html')

def searchimpl(request):
    try:
        rela = request.POST['rela']
        data2 = similarity_word(rela)
        print(data2)
        context = { 'data2' : HttpResponse(json.dumps(data2), content_type='application/json') }
        return render(request, 'search2.html', context)
    except Exception as err:
        print(err)
        context = {'msg': ErrorCode.e03}
        return render(request, 'index.html', context)

def moreinfo(request):
    return render(request, 'moreinfo.html')

def chart_KIM(request):
    mon = request.GET['mon'];
    data_KIM = keywordissuemap_KIM(mon);
    return HttpResponse(json.dumps(data_KIM), content_type='application/json');

def chart_KEM(request):
    mon = request.GET['mon'];
    data_KEM = keywordissuemap_KEM(mon);
    return HttpResponse(json.dumps(data_KEM), content_type='application/json');

def chart2(request):
    rela = request.GET['rela'];
    data2 = similarity_word(rela);
    return HttpResponse(json.dumps(data2), content_type='application/json');

def chart3(request):
    data3 = [29.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4]
    return HttpResponse(json.dumps(data3), content_type='application/json');

def trend(request):
    return render(request, 'trend.html')
