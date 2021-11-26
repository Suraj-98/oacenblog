from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login 
from django.views import View
from .models import Comment, UpdateProfileImage, User,Image,Like
from .forms import  NewUserForm,CustomAuthenticationForm,ImageForm,UserDetailsForm,UpdateProfileImageForm,CommentForm 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
def indexpage(request):
    return render(request,"index.html")

@login_required(login_url="http://localhost:8000/website/signinpage")
def homepage(request):
    img=Image.objects.all().order_by('date_created')    
    return render(request,"home.html",{'img':img})

def signuppage(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            send_mail(
    'create account',
    'successfully created your account',
    settings.EMAIL_HOST_USER,
    ['surajsharma3050@gmail.com'],
    fail_silently=False
)
            return redirect("/website/signinpage/")
 
    form = NewUserForm()    
    obj=User.objects.all()
    return render(request,"signup.html",{'form':form})
    
    
def signinpage(request):

    if request.method=='POST':
        form=CustomAuthenticationForm(request=request,data=request.POST)
        if form. is_valid():
            uname=form.cleaned_data["username"]
            pname=form.cleaned_data["password"]
            user=authenticate(username=uname,password=pname)
            if user is not None:
                login(request,user)
                request.session["msg"]="successful login"
                request.session["login"]=uname
                messages.success(request,"Signin successfully")
                return redirect("/website/homepage/")
                

    else:
        form=CustomAuthenticationForm()
    return render(request,"signinpage.html",{'form':form})


def signoutpage(request):
    del request.session["msg"]
    del request.session["login"]
    return redirect("http://localhost:8000/website/signinpage")

@csrf_exempt
def profilepage(request):
    pf=UpdateProfileImage.objects.filter(user=request.user)
    img=Image.objects.filter(user=request.user)
    return render(request,"profile.html",{'pf':pf,'img':img})

@login_required(login_url="http://localhost:8000/website/signinpage")
def postpage(request):
    
    if request.method == 'POST':
        form =ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            return redirect("http://localhost:8000/website/homepage")
       
    
    form=ImageForm()
    img=Image.objects.filter(user=request.user) 
    return render(request,"post.html",{'img':img,'form':form})    

@login_required(login_url="http://localhost:8000/website/signinpage")
def updateprofile(request):
    if request.method == 'POST':
        form1=UpdateProfileImageForm(request.POST,request.FILES,instance=request.user)
        form =UserDetailsForm(request.POST,instance=request.user)
        if form1.is_valid() and form.is_valid():
            form1.save()
            form.save()
    
            
            return redirect("http://localhost:8000/website/profilepage")
    form1=UpdateProfileImageForm(instance=request.user)
    form=UserDetailsForm(instance=request.user)
    return render(request,"updateprofile.html",{'form1':form1,'form':form})

@login_required(login_url="http://localhost:8000/website/signinpage")
def changepassword(request):
    if request.method == "POST":
        form=PasswordChangeForm(data=request.POST,user=request.user)
        if form.is_valid():
            form.save()
            return redirect("/website/signinpage")
    form=PasswordChangeForm(user=request.user)
    return render(request,"changepassword.html",{'form':form})

@login_required(login_url="http://localhost:8000/website/signinpage")
def like(request,id):
    p = Image.objects.get(pk=id)
    likes = Image.objects.filter(user=request.user) and True or False
    return redirect("/website/homepage",{"likes":likes})
    
@login_required(login_url="http://localhost:8000/website/signinpage")
def postdetail(request,id):
    if request.method == "POST":
        form=CommentForm(request.POST)
        if form.is_valid():
            form.save()
    cm=Comment.objects.all().filter(image=id)
    post=Image.objects.filter(pk=id)
    form=CommentForm()
    return render(request,"postdetail.html",{"post":post,"form":form,"cm":cm})

@login_required(login_url="http://localhost:8000/website/signinpage")
def delete(request,id):
    pi=Image.objects.filter(pk=id)
    pi.delete()
    return redirect("/website/homepage")