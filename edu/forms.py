from django import forms
from .models import User

class TeacherSearchForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=False, label='نام')
    last_name = forms.CharField(max_length=50, required=False, label='نام خانوادگی')
    from_date = forms.DateField(required=False, label='از تاریخ')
    to_date = forms.DateField(required=False, label='تا تاریخ')
    profession = forms.CharField(max_length=50, required=False, label='تخصص')

# class LoginForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username' , 'password']