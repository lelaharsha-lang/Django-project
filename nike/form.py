# forms.py
from symtable import Class
from django import forms
from app1.models import User
from .models import Blog

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'image', 'mobile_number', 'password']
        widgets = {
            'password':forms.PasswordInput(),
        } # include all fields from the model

    def save(self, commit = True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title','content','picture' ]
 