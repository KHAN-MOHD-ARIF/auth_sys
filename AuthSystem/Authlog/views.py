from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from AuthSystem.email import *
from .models import *
import uuid
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def sign_up(request):
    if request.method=='POST':
        username=request.POST['uname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        print(username,email,pass1,pass2)
        if pass1!=pass2:
            messages.error(request,'confirm password is not matched!')
            return redirect('signup')
        elif User.objects.filter(username=username).exists():
            messages.info(request,'username already taken!')
            return redirect('signup')
        elif User.objects.filter(email=email).exists():
            messages.info(request,'email Id already taken!')
            return redirect('signup')
        my_user=User(username=username,email=email)
        my_user.set_password(pass1)
        my_user.save()
        email_token=str(uuid.uuid4())
        pro_file=Profile.objects.create(user=my_user,email_token=email_token)
        pro_file.save()
        send_email_token(email,email_token)
        messages.success(request,f'{username} your account has been created successfully.\n An email has been send to your register email id\n please verify it before login.')
        return redirect('login')

    return render(request,'signup.html')

def Log_in(request):
    if request.method=='POST':
        username=request.POST['uname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        # print(username,email,pass1)
        my_user=User.objects.filter(username=username).first()
        # print('**',my_user1)
        if my_user is None:
            messages.success(request,'users not found!')
            return redirect('login')
        my_prof=Profile.objects.filter(user=my_user).first()
        if not my_prof.is_email_verified:
            messages.success(request,"You'r not verified, Please check your mail!")
            return redirect('login')
        user_auth=authenticate(username=username,password=pass1,email=email)
        if user_auth is None:
            messages.info(request,'password or username is incorrect!')
            return redirect('login')
        else:
            login(request,user_auth)
            messages.info(request,'socksess')
            return redirect('home')

    
            


    return render(request,'login.html')

def veri_fy(request,token):
    try:
        prof=Profile.objects.get(email_token=token)
        if prof.is_email_verified:
            messages.info(request,'You are already verified!')
            return redirect('login')
        prof.is_email_verified=True
        prof.save()
        messages.success(request,'Hurry!, your account has been verified')
        return redirect('login')
    except Exception as e:
        return HttpResponse('invalid token')

@login_required(login_url='login')
def homepage(request):
    return render(request,'homepage.html')

@staff_member_required
def sta_ff(request):
    return render(request,'staff.html')

def log_out(request):
    logout(request)
    return redirect('login')



