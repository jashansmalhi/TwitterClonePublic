from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User




class CreateUserForm(UserCreationForm):

    class Meta:
        model=User
        fields=['username','password1','password2']

    def __int__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            new_data={
                'class':'form-control'
            }
            self.fields[str(field)].widgets.attrs.update(new_data)

