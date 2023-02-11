from django import forms
from .models import Post
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class PostForm(forms.ModelForm):
    class Meta:
       model = Post
       fields = [
           'field',
           'header',
           'text',
           'category'
       ]

   # def clean(self):
    #    cleaned_data = super().clean()
     #   header = cleaned_data.get('header')
      #  if header is not None and len(header) < 20:
       #     raise ValidationError({
        #        'header': "Заголовок не может быть менее 20 символов"
         #   })
#
 #       return cleaned_data


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
