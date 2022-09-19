from django.urls import path
from . import views

urlpatterns=[
    path('login', views.loginPage,name='login'),
    path('',views.home,name = 'home'),
    path('personal',views.homePersonal,name='personal'),
    path('reg', views.regPage,name='reg'),
    path('logout',views.logoutPage,name='logout'),
    path('profile',views.profilePage,name='profile'),
    path('profile/edit',views.editProfile,name='edit'),
    path('tweet/delete/<int:id>',views.deleteTweetUser,name='deletee'),
    path('profile/<str:username>',views.nonUserProfile,name='nonuserprofile'),
    path('follow/<str:username>',views.follow,name='follow'),
    path('unfollow/<str:username>',views.unfollow,name='unfollow'),
    path('profile/<str:username>/followers',views.followers,name='followers'),
    path('profile/<str:username>/following',views.following,name='following'),
    path('search',views.search,name='search'),
    path('tweet/<int:id>',views.tweet,name = 'tweet'),
    path('tweet/<int:tweetid>/delete/<int:id>',views.deletecomment,name = 'deletecomment'),
    path('tweet/<int:tweetid>/like',views.liketweet,name='like')
]
