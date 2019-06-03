from django import forms
from django.forms import ModelForm
from .models import Student, Register


class TeacherSearchForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=False, label='نام')
    last_name = forms.CharField(max_length=50, required=False, label='نام خانوادگی')
    profession = forms.CharField(max_length=50, required=False, label='تخصص')
    DIPLOMA, ASSOCIATE, BACHELOR, MASTER, PHD = 'DP', 'AS', 'BA', 'MA', 'PHD'
    degree_choices = (
        (DIPLOMA, 'دیپلم'),
        (ASSOCIATE, 'فوق دیپلم'),
        (BACHELOR, 'لیسانس'),
        (MASTER, 'فوق لیسانس'),
        (PHD, 'دکتری')
    )
    education_degree = forms.ChoiceField(choices=degree_choices, required=False, label='مدرک تحصیلی')


class StudentSearchForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=False, label='نام')
    last_name = forms.CharField(max_length=50, required=False, label='نام خانوادگی')
    birth_date = forms.CharField(max_length=10,required=False, label='تاریخ تولد')
    FIRST, SECOND, THIRD = 'first', 'second', 'third'
    level_choices = (
        (FIRST, 'اول'),
        (SECOND, 'دوم'),
        (THIRD, 'سوم')
    )

    level = forms.ChoiceField(choices=level_choices)

    MATH, NATURAL, HUMANITY = 'math', 'natural', 'humanity'
    field_choices = (
        (MATH, 'ریاضی'),
        (NATURAL, 'تجربی'),
        (HUMANITY, 'انسانی')
    )
    field = forms.ChoiceField(choices=field_choices)







class ClassroomSearchForm(forms.Form):
    A, B, C = 'a', 'b', 'c'
    branch_choices = (
        (A, 'الف'),
        (B, 'ب'),
        (C, 'ج')
    )
    branch = forms.ChoiceField(choices=branch_choices)
    education_year = forms.CharField(max_length=20, required=False)

class RegisterForm(forms.ModelForm):

    class Meta:
        model = Register
        fields = '__all__'

class StudentCreateViewForm(forms.ModelForm):

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
    birth_date = forms.CharField(required=False)
    image = forms.ImageField()


    class Meta:
        model = Student
        fields = [ 'student_id', 'image', 'birth_date']

    def save(self, commit=True):
        return super(StudentCreateViewForm, self).save(commit=commit)


# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username' , 'password']

#
# class TeacherCreateViewForm(forms.ModelForm):
#
#     class Meta:
#         model = Teacher
#         fields = ['profession']
#
#     def __init__(self, *args, **kwargs):
# self.user = kwargs.pop('user')
# super(TeacherCreateViewForm, self).__init__(*args, **kwargs)
#
# def save(self):
#     result = super(TeacherCreateViewForm, self).save(commit=False)
#     result.creator = self.user
#     result.approver = self.user.first_name  # "will be set also set automatically"
#     result.save()
#     return result
