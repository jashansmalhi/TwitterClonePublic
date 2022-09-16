from django.contrib import admin
from .models import Followers,Tweets,Account


# Register your models here.
admin.site.register(Account)
admin.site.register(Followers)
admin.site.register(Tweets)