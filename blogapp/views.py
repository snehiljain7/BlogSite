from django.shortcuts import render
from blogapp.models import Blog
from blogapp.forms import BlogForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.
def home(request):
    return render(request, 'blogapp/home.html')

@login_required
def addblog(request):
    blogform = BlogForm()
    mydict = {'blogform': blogform}
    if request.method == 'POST':
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            data = blogform.save()
            data.author = str(request.user)
            data.save()
            mydict.update({'msg': 'Blog Added successfully'})
    return render(request, 'blogapp/addblog.html', context = mydict)

def ViewBlog(request):
    images = Blog.objects.all().order_by('-upload_date')
    mydict = {'images': images}
    return render(request, 'blogapp/viewblog.html', context=mydict)
@login_required
def detailblog(request, id):
    images = Blog.objects.get(id = id)
    return render(request, 'blogapp/detailblog.html', {'images': images})

def deleteblog(request, pid):
    images = Blog.objects.get(id = pid)
    images.delete()
    images = Blog.objects.all().order_by('-upload_date')
    mydict = {'images': images}
    return render(request, 'blogapp/viewblog.html', {'images': images})

def SignUp(request):
    signupform = SignUpForm()
    mydict = dict()
    if request.method == 'POST':
        signupform = SignUpForm(request.POST)
        if signupform.is_valid():
            user = signupform.save()
            user.set_password(user.password)
            user.save()
            subject = "Welcome to the Blog Site"
            message = "Welcome "+user.first_name+", You have registered successfully"
            recipient_list = [user.email]
            email_from = settings.EMAIL_HOST_USER
            send_mail (subject, message, email_from, recipient_list)
            mydict.update({'msg': 'Registered successfully'})
    mydict.update({'signupform': signupform})
    return render(request, 'blogapp/signup.html', context = mydict)
