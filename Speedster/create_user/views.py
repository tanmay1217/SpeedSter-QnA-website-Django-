from django.shortcuts import render,redirect
from .forms import user_create
from django.contrib.auth.models import User
from .forms import user_create
from .models import Question,Answer
from .models import QuestionForm,AnswerForm
from django.urls import reverse
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage


# Create your views here.

def home(request):
    current_user = request.user
    #print(current_user)
    questions=Question.objects.all().order_by('-created')
    all_questions=Question.objects.all()
    #print(all_questions)
    page =request.GET.get('page',1)
    paginator =Paginator(all_questions,7)
    try:
        show_q=paginator.page(page)
        #print(show_q)
    except PageNotAnInteger:
        show_q =paginator.page(1)
    except EmptyPage:
        show_q =paginator.page(paginator.num_pages)
    return render(request,'home.html',{'question':questions,'show_q':show_q})


def signup(request):
    form=user_create()
    #print('hello')
    if request.method =="POST":
        form = user_create(request.POST)
        if form.is_valid():
            user_name=form.cleaned_data['user_name']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            user = user=User.objects.create_user(username=user_name,email=email,password=password)
            user.save()
            return redirect('/')
            #another way to check if username exists or not
            '''
            try:
                user =User.objects.get(username =user_name)
                context= {'form': form,
                 'error':'The username you entered has already been taken. Please try another username.'}
                return render(request,'registration/signup.html',context)
            except User.DoesNotExist:
                user = user=User.objects.create_user(username=user_name,email=email,password=password)
                user.save()
                return redirect('/')
                '''
    return render(request,'registration/signup.html',{'title':'SignUp','form':form})


def question_view(request,id):
    current_user =request.user
    asked_by_user=False
    quest = Question.objects.get(pk=id)
    #print(quest,quest.user,quest.user_id,current_user.id,current_user)
    answers = Answer.objects.filter(question=quest).order_by('created')
    answer_form =AnswerForm()
    if current_user.id == quest.user_id:
        asked_by_user =True
    context ={'qst':quest,'ans':answers,'current_user':current_user,
            'asked_by_user':asked_by_user,'form':answer_form,
            }
    return render(request,'questions.html',context)


def new_question(request):
    current_user=request.user
    if not current_user.is_authenticated:
        return redirect('login')
    form_question = QuestionForm()
    if request.method == "POST":
        form_question = QuestionForm(request.POST)
        if form_question.is_valid():
            Question.objects.get_or_create(
            user_id =current_user.id,       #this is compulsly
            title =form_question.cleaned_data['title'],
            body =form_question.cleaned_data['body'],)

            #   or     #
            #q=Question(user_id=current_user.id,
            #title=form_question.cleaned_data['title'],
            #body =form_question.cleaned_data['body']
            #)
            #q.save()
            #   end or     #

            return redirect('home')
    return render(request,'form_question.html',{'form':form_question,'current_user':current_user})



def my_question_view(request):
    current_user =request.user
    if not current_user.is_authenticated:
        return redirect('login')
    #print(current_user)
    question=Question.objects.filter(user_id = current_user.id)
    #print(question)
    is_question_asked =len(question) >0
    return render(request,'my_question.html',{'current_user':current_user,'questions':question,'is_question_asked':is_question_asked})


def answer_view(request,id):
    current_user = request.user
    if request.method =="POST":
            form =AnswerForm(request.POST)
            #print(id)
            if form.is_valid():
                a=Answer(
                user_id =current_user.id,
                question_id = id,
                text =form.cleaned_data['text']
                )
                a.save()
                return redirect('question',id)
