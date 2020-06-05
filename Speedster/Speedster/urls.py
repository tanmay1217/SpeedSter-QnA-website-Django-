"""Speedster URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include
from create_user import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('accounts/signup/',views.signup,name='signup'),
    path('accounts/',include('django.contrib.auth.urls')),
    path('quest/<int:id>',views.question_view,name='question'),
    path('question/new/',views.new_question,name='new_question'),
    path('questions/my_question',views.my_question_view,name='my_question_view'),
    path('answer/<int:id>',views.answer_view,name='answer_view'),

]
