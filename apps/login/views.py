from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.db.models import Count
def index(request):
    context={
        'users':User.objects.all()
    }
    return render(request, 'login/index.html',context)
def process(request):
     # pass the post data to the method we wrote and save the response in a variable called errors
    errors = User.objects.basic_validator(request.POST)
        # check if the errors object has anything in it

    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    
    else:
        # if the errors object is empty, that means there were no errors!
        # retrieve the user to be updated, make the changes, and save
        User.objects.Create_user(request.POST)

        request.session['email']=request.POST['email']

        messages.success(request, "User successfully added")
        # redirect to a success route
        return redirect('/wall')
def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')

    request.session['email']=request.POST['email']

    return redirect('/wall')
def wall(request):
    context={
        'posts':Message.objects.all(),
        'user':User.objects.all().get(email=request.session['email'])
    }
    return render(request, 'login/wall.html', context)
def addmessage(request):
    errors = Message.objects.basic_validator(request.POST)
    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/wall')
    Message.objects.Create_message(request.POST)
    return redirect('/wall')
def like(request,postid,userid):
    if 'email' not in request.session:
        return redirect('/')
    post=Message.objects.get(id=postid)
    user=User.objects.get(id=userid)
    try:
        Check_if_Liked = post.likes.get(user_id=userid,message_id=postid)
    except:
        flag=False
    if flag is False:
        post.likes.add(user)
    return redirect('/wall')
def popular(request):
    user=User.objects.get(email=request.session['email'])
    context={
        'posts':Message.objects.annotate(like_count=Count('likes')).order_by('-like_count'),
        'user':user
    }
    return render(request,'login/popular.html',context)