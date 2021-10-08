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

def sign_up(request):
    return render(request, 'sign-up.html')
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

def search2(request):
    return render(request, 'search2.html')

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
    KE_SS = keywordMap(mon)[2];
    KE_WS = keywordMap(mon)[3];
    KE_LS = keywordMap(mon)[4];
    KE_WKS = keywordMap(mon)[5];
    KI_SS = keywordMap(mon)[6];
    KI_WS = keywordMap(mon)[7];
    KI_LS = keywordMap(mon)[8];
    KI_WKS = keywordMap(mon)[9];
    context = {'signals1': KE_SS, 'signals2': KE_WS, 'signals3': KE_LS, 'signals4': KE_WKS,
               'signals5': KI_SS, 'signals6': KI_WS, 'signals7': KI_LS, 'signals8': KI_WKS}
    return render(request, 'index.html', context)
