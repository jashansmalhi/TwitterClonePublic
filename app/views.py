from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, TweetForm
from .models import Tweets,Account,Followers
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

def regPage(request):
    logout(request)
    form = CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'User Created.')
            return redirect('/login')
    context = {'form':form}
    return render(request,'signup.html',context)

def loginPage(request):
    logout(request)
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request, 'Wrong Credentials.')
            return redirect('login')

    return render(request,'login.html')

def logoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    user = request.user
    user_following=Followers.getFollowing(user)
    print(user_following)

    if request.method=='POST':
        message =  request.POST.get('tweet')
        tweet=Tweets(text=message,tweeter=user)
        tweet.save()
        return redirect('home')
    tweets = Tweets.objects.order_by('-time')
    return render(request,'home.html',{'tweets':tweets,'user_following':user_following})


@login_required(login_url='login')
def homePersonal(request):
    user = request.user
    usernames_following=Followers.getFollowing(user)
    users_following = User.objects.filter(username__in=usernames_following)
    tweets=Tweets.objects.filter(tweeter__in=users_following).order_by('-time')
    print(users_following)
    if request.method=='POST':
        message = request.POST.get('tweet')
        tweet=Tweets(text=message,tweeter=user)
        tweet.save()
        return redirect('home')
    return render(request,'home.html',{'tweets':tweets,'user_following':users_following})


@login_required(login_url='login')
def nonUserProfile(request,username):
    currentUser=request.user
    user=User.objects.filter(username=username).first()


    followers=Followers.getFollowers(user)

    if followers and currentUser in followers:
        isfollowing=True
    else:
        isfollowing=False

    if user == request.user:
        return redirect('profile')
    usertweets = Tweets.AllTweets(user)
    accinfo = Account.findAccountInfo(user)
    if user:
        return render(request,'nonUserProfile.html',{'tweets':usertweets,
                                          'user':user,
                                          'numtweets':Tweets.NumberOfTweets(user),
                                          'followers':Followers.NumberOfFollowers(user),
                                          'following':Followers.NumberOfFollowed(user),
                                          'accInfo':accinfo,'isfollowing':isfollowing})
    return redirect('profile')

@login_required(login_url='login')
def profilePage(request):
    user  = request.user
    accinfo = Account.findAccountInfo(user)
    if request.method=='POST':
        message =  request.POST.get('tweet')
        tweet=Tweets(text=message,tweeter=user)
        tweet.save()
        return redirect('profile')
    usertweets = Tweets.AllTweets(user)
    return render(request,'profile.html',{'tweets':usertweets,
                                          'user':user,
                                          'numtweets':Tweets.NumberOfTweets(user),
                                          'followers':Followers.NumberOfFollowers(user),
                                          'following':Followers.NumberOfFollowed(user),
                                          'accInfo':accinfo})

@login_required(login_url='login')
def editProfile(request):
    user = request.user
    accinfo = Account.findAccountInfo(user)
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        bio = request.POST.get('bio')
        if user.username!=username:
            if User.objects.filter(username=username).first():
                messages.info(request,'Username already taken.')
                return redirect('edit')
        if accinfo:
            accinfo.name=name
            accinfo.bio=bio
            accinfo.save()
            user.username=username
            user.save()
            return redirect('profile')
        else:
            accinfo = Account(user = user,name = name,bio=bio)
            accinfo.save()
            user.username = username
            user.save()
        return redirect('profile')
    return render(request,'editprofile.html',{'user':user,'accinfo':accinfo})

@login_required(login_url='login')
def followers(request,username):
    accounts = Followers.getFollowers(username)
    return render(request,'followers.html',{'accounts':accounts})

@login_required(login_url='login')
def following(request,username):
    user=User.objects.filter(username=username).first()
    accounts = Followers.getFollowing(user)
    return render(request, 'followers.html', {'accounts': accounts})

@login_required(login_url='login')
def follow(request,username):
    if Followers.objects.filter(follower=request.user,followed=username):
        return redirect(nonUserProfile,username=username)
    followed = Followers(follower=request.user,followed=username)
    followed.save()
    return redirect(nonUserProfile,username=username)

@login_required(login_url='login')
def unfollow(request,username):
    data = Followers.objects.get(follower=request.user, followed=username)
    if data:
        data.delete()
    return redirect(nonUserProfile,username=username)

@login_required(login_url='login')
def deleteTweetHome(request,id):
    tweet = Tweets.objects.filter(id=id).first()
    if tweet.tweeter == request.user:
        tweet.delete()
    return redirect('home')

@login_required(login_url='login')
def deleteTweetUser(request,id):
    tweet = Tweets.objects.filter(id=id).first()
    if tweet.tweeter == request.user:
        tweet.delete()
    return redirect('profile')

@login_required(login_url='login')
def search(request):
    if request.method=='POST':
        keyword = request.POST.get('keyword')
        results = User.objects.filter(username__icontains=keyword)
        return render(request,'search.html',{'results':results})
    return redirect('home')

