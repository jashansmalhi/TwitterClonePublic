from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    bio = models.CharField(max_length=140)

    @classmethod
    def findAccountInfo(cls, user):
        return cls.objects.filter(user=user).first()

class Followers(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE,related_name='related_primary_manual_roats')
    followed = models.ForeignKey(User, on_delete=models.CASCADE,related_name='related_secondary_manual_roats')
    @classmethod
    def getFollowing(cls,user):
        followedd = []
        un = cls.objects.filter(follower=user)
        for follow in un:
            followedd.append(follow.followed)
        return followedd
    @classmethod
    def getFollowers(cls,user):
        followers = []
        un = cls.objects.filter(followed=user)
        for follower in un:
            followers.append(follower.follower)
        return followers

    @classmethod
    def NumberOfFollowers(cls,user):
        return cls.objects.filter(followed=user).count()

    @classmethod
    def NumberOfFollowed(cls,user):
        return cls.objects.filter(follower=user).count()



class Tweets(models.Model):
    text = models.CharField(max_length=140)
    tweeter = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    def likers(self):
        print(Likes.objects.filter(tweet_id=self.id).values_list('liker', flat=True))
        return Likes.objects.filter(tweet_id=self.id).values_list('liker', flat=True)

    def numlikes(self):
        return Likes.objects.filter(tweet=self.id).count()
    def numcomments(self):
        return Comments.objects.filter(tweet=self.id).count()

    @classmethod
    def NumberOfTweets(cls,user):
        return cls.objects.filter(tweeter=user).count()

    @classmethod
    def AllTweets(cls,user):
        return cls.objects.filter(tweeter=user).order_by('-time')


class Likes(models.Model):
    tweet=models.ForeignKey(Tweets, on_delete=models.CASCADE)
    liker = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def NumberOfLikes(cls,tweet):
        return cls.objects.filter(tweet=tweet).count()

class Comments(models.Model):
    tweet=models.ForeignKey(Tweets, on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=140)
    time = models.DateTimeField(auto_now_add=True)

    @classmethod
    def NumberOfComments(cls,tweet):
        return cls.objects.filter(tweet=tweet).count()

    @classmethod
    def AllComments(cls,tweet):
        return cls.objects.filter(tweet=tweet).order_by('-time')