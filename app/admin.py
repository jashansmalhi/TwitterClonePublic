from django.contrib import admin
from .models import Followers,Tweets,Account,Comments,Likes


# Register your models here.
admin.site.register(Account)
admin.site.register(Followers)
admin.site.register(Tweets)
admin.site.register(Comments)
admin.site.register(Likes)