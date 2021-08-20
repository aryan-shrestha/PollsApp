from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import *
# Create your views here.

def index(request):
    questions = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    context = {
        'questions' : questions,
    }
    return render(request, 'pollsapp/index.html', context)

@login_required
def detail(request, pk):
    question = get_object_or_404(Question, id=pk)
    pk = pk
    context = {
        'question': question
    }
    return render(request, 'pollsapp/detail.html', context)

@login_required
def vote(request, pk):
    question = get_object_or_404(Question, id=pk)
    try:
        choice = question.choice_set.get(id = request.POST['choice']) # request.POST['*name_attribute'] return the value of input field
    except: # executes the following codes if any errors
        context = {
            'question': question,
            'error_message': "You didn't select a choice.",
        }
        return render(request, 'pollsapp/detail.html', context)
    else:  # executes the following code if no errors
        choice.votes +=1
        choice.save()
        return HttpResponseRedirect(reverse('pollsapp:index'))
@login_required
def add_polls(request):
    if request.method == 'POST':
        question = request.POST['question_text']
        user = request.user
        print(user)
        q = Question.objects.create(user = user,question_text=question)
        for i in range(1,5):
            choice = request.POST[f'choice-{i}']
            if choice == '':
                continue
            else:
                c = q.choice_set.create(choice_text= choice)
            
        return HttpResponseRedirect(reverse('pollsapp:index'))
    else:
        return render(request, 'pollsapp/add_polls.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            first_name = request.POST['first-name']
            last_name = request.POST['last-name']
            email = request.POST['email']
            password = request.POST['password']
            new_user = User.objects.create_user(username, email, password)
            new_user.first_name = first_name
            new_user.last_name =last_name
            new_user.save()
            context = {
                'success_message': 'User created. Use the credentials to login.'
            }
            return HttpResponseRedirect(reverse('pollsapp:login'),context)
        else:
            context = {
                'error_message': 'username already exists. Try another username.'
            }
            return render(request, 'pollsapp/register.html', context)
    else:
        return render(request, 'pollsapp/register.html')

def user_login(request):
    if request.method == 'POST':    
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("authenticated")
            return HttpResponseRedirect(reverse('pollsapp:index'))
        else:
            print("Not authenticated")
            context = {
                'error_message':"Invalid Username or password!!"
            }
            return render(request, 'pollsapp/login.html', context)
    else:
        return render(request, 'pollsapp/login.html')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('pollsapp:index'))

@login_required
def my_polls(request):
    user_name = request.user
    user = User.objects.get(username=user_name)
    polls = user.question_set.all().order_by('-pub_date')[:5]
    no_of_votes = polls.count()
    context = {
        'user':user, 
        'polls':polls,
        'no_of_votes': no_of_votes,
    }
    return render(request, 'pollsapp/my_polls.html', context)

@login_required
def result(request, pk):
    question = get_object_or_404(Question, id = pk)

    context = {
        'question': question,
    }
    return render(request, 'pollsapp/result.html', context)
