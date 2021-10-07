"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from vihotest2 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    path('login_two', views.login_two, name='login_two'),
    path('loginimpl', views.loginimpl, name='loginimpl'),
    path('logout', views.logout, name='logout'),
    path('forget_password', views.forget_password, name='forget_password'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('sign_up_one', views.sign_up_one, name='sign_up_one'),
    path('sign_up_two', views.sign_up_two, name='sign_up_two'),
    path('signupimpl', views.signupimpl, name='signupimpl'),
    path('search', views.search, name='search'),
    path('search2', views.search2, name='search2'),
    path('general_widget', views.general_widget, name='general_widget'),
    path('update', views.update, name='update'),
    path('infoupdate', views.infoupdate, name='infoupdate'),
    path('introduce', views.introduce, name='introduce'),
    path('searchimpl', views.searchimpl, name='searchimpl'),
    path('moreinfo', views.moreinfo, name='moreinfo'),
    path('chart_KIM', views.chart_KIM, name='chart_KIM'),
    path('chart_KEM', views.chart_KEM, name='chart_KEM'),
    path('chart2', views.chart2, name='chart2'),
    path('chart3', views.chart3, name='chart3'),
    path('trend', views.trend, name='trend'),
    path('signal', views.signal, name='signal'),
    path('sad', views.sad, name='sad'),

]
