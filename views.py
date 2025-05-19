from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from random import randrange
from .models import ProfileModel

def login_view(request):
    if request.method == "POST":
        un = request.POST.get("un")
        pw = request.POST.get("pw")
        print(f"Attempting login with username: {un} and password: {pw}")
        try:
            user = User.objects.get(username=un)
            print(f"User found: {user}")
            usr = authenticate(username=un, password=pw)
            if usr is not None:
                print("Authentication successful")
                auth_login(request, usr)
                return redirect("home")
            else:
                print("Authentication failed")
                messages.error(request, "Invalid login")
        except User.DoesNotExist:
            print("User does not exist")
            messages.error(request, "Invalid login")
        return render(request, "login.html", {"msg": "Invalid login"})
    else:
        return render(request, "login.html")

def signup(request):
    if request.method == "POST":
        un = request.POST.get("un")
        ph = request.POST.get("ph")
        try:
            usr=User.objects.get(username=un)
            return render(request, "signup.html", {"msg": "username already exists, please choose another username"})
        except User.DoesNotExist:
            try:
                usr = ProfileModel.objects.get(phone=ph)
                return render(request, "signup.html", {"msg": "Phone already exists, please choose another username"})
            except ProfileModel.DoesNotExist:
                pw = ""
                txt = "0123456789"
                for i in range(4):
                    pw += txt[randrange(len(txt))]
                print(pw)
                send_sms(ph, pw)
                usr = User.objects.create_user(username=un, password=pw)
                usr.save()
                pro = ProfileModel(user=usr, phone=ph)
                pro.save()
                return redirect("login_view")
    else:
        return render(request, "signup.html")

def logout_view(request):
    auth_logout(request)
    return redirect("login_view")

@login_required
def home(request):
    return render(request, "home.html")

def changepw(request):
    if request.method == "POST":
        un = request.POST.get("un")
        pw1 = request.POST.get("pw1")
        pw2 = request.POST.get("pw2")
        if pw1 == pw2:
            try:
                usr = User.objects.get(username=un)
                usr.set_password(pw1)
                usr.save()
                return redirect("login_view")
            except User.DoesNotExist:
                return render(request, "changepw.html", {"msg": "User does not exist"})
        else:
            return render(request, "changepw.html", {"msg": "Passwords do not match"})
    return render(request, "changepw.html")

def rnp(request):
    if request.method == "POST":
        un = request.POST.get("un")
        try:
            usr = User.objects.get(username=un)
            pw = ""
            txt = "0123456789"
            for i in range(4):
                pw += txt[randrange(len(txt))]
            print(pw)
            subject = "Password Reset Request"
            msg = f"Your new password is {pw}"
            send_mail(subject, msg, settings.EMAIL_HOST_USER, [usr.email])
            usr.set_password(pw)
            usr.save()
            messages.success(request, "A new password has been sent to your email.")
            return redirect("login_view")
        except User.DoesNotExist:
            messages.error(request, "Username does not exist")
            return render(request, "rnp.html")
    else:
        return render(request, "rnp.html")

def send_sms(ph,pw):
    import requests
    url="https://www.fast2sms.com/dev/bulkV2"
    querystring={
        "authorization":"xdGVgouQ7PBO1lpTYUvwaKHhbjeWDq5S3XRyAtFkNz6M9mCs4EZWofKOtq3zh7Mue41LGYarFPi82cw6",
        "sender_id":"kaushal",
        "message":"Ur password is "+str(pw),
        "route":"p",
        "numbers":str(ph),
    }
    res=requests.request("GET",url,params=querystring)
    print(res)

# Create your views here.
