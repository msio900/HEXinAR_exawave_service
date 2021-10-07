import json
import pickle

from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
from analysis.keywordissuemap import keywordissuemap_KIM, keywordissuemap_KEM, similarity_word, searchKeywords
from analysis.test import keywordMap
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
        context = { 'data2' : data2 }
        return render(request, 'search2.html', context)
    except Exception as err:
        print(err)
        context = {'msg': ErrorCode.e03}
        return render(request, 'index.html', context)

def moreinfo(request):
    return render(request, 'moreinfo.html')

def chart_KIM(request):
    mon = request.GET['mon'];
    mon = mon.replace(' ', '')
    data_KIM = keywordissuemap_KIM(mon);
    return HttpResponse(json.dumps(data_KIM), content_type='application/json');

def chart_KEM(request):
    mon = request.GET['mon'];
    mon = mon.replace(' ', '')
    data_KEM = keywordissuemap_KEM(mon);
    return HttpResponse(json.dumps(data_KEM), content_type='application/json');

def chart2(request):
    rela = request.GET['rela'];
    data2 = similarity_word(rela);
    return HttpResponse(json.dumps(data2), content_type='application/json');

def chart3(request):
    rela = request.GET['rela'];
    category = searchKeywords(rela)[0];
    tf_word_nums = searchKeywords(rela)[1];
    df_word_nums = searchKeywords(rela)[2];
    data3 = [category, tf_word_nums, df_word_nums]
    return HttpResponse(json.dumps(data3), content_type='application/json');
def trend(request):
    return render(request, 'trend.html')

def signal(request):
    mon = request.GET['mon'];
    mon = mon.replace(' ', '')
    data_signal = keywordMap(mon)[2];
    context = {'signals': data_signal}
    print(context)
    return render(request, 'index.html', context)


def sad(request):
    data_signals = ['유수인', '정두현', '마트료시카', '모문룡', '리펜슈탈', '정순철', '박영발', '쇼블', '스웬슨', '테메노스']
    context = {'signals': data_signals }
    print(context)
    return render(request, 'sad.html', context)