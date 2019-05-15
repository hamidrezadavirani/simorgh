from urllib import request
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Student, Classroom, Teacher
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from edu import forms
from django.db.models import Q
from .serializers import StudentSerializer
from django.http import JsonResponse
from django.contrib.auth.views import LoginView
import urllib.request


def display_dashboard(request):
    return render(request, 'edu/dashboard.html', {})

def display_main(request):
    current_user = request.user
    print (current_user)
    return render(request,'edu/main.html', {})


def students_show(request):
    if request.method == 'GET':
        students = Student.objects.all()
        serialized = StudentSerializer(students, many=True)
        return JsonResponse(serialized.data, safe=False)


def about_us(request):
    return render(request, 'edu/about_us.html', {})

def contact_us(request):
    return render(request, 'edu/contact_us.html', {})

def class_list(request, class_id):
    classroom = Classroom.objects.filter(id=class_id).first()
    classroom_students = list(Student.objects.filter(classroom=classroom))
    return render(request, 'edu/student_list.html', {'classroom_student': classroom_students})

class login(LoginView):

    template_name = 'edu/main.html'
    success_url = '/teachers'
    # form_class = forms.LoginForm


class StudentListView(ListView):
    model = Student


class StudentCreateView(CreateView):
    model = Student
    fields = ['student_id', 'user', 'last_modified_date']
    success_url = '/class/students/create/'


class TeacherListView(ListView):
    model = Teacher


    def get_context_data(self, **kwargs):
        context = super(TeacherListView, self).get_context_data(**kwargs)
        form = forms.TeacherSearchForm()
        context['form'] = form
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        first_name = self.request.GET.get('first_name')
        last_name = self.request.GET.get('last_name')
        if self.request.GET and any([first_name, last_name]):
            queryset = queryset.filter(Q(user__first_name=first_name) | Q(user__last_name=last_name))
        return queryset


class TeacherCreateView(CreateView):
    model = Teacher
    fields = '__all__'
    success_url = '/class/teachers/create/'


class ClassroomListView(ListView):
    model = Classroom


class ClassroomCreateView(CreateView):
    model = Classroom
    fields = ['level_field', 'branch', 'education_year']
    success_url = '/class/classrooms/create/'


class ClassroomDetailView(DetailView):
    model = Classroom
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context

# class StudentUpdateView(UpdateView):
#     model = Student
#     fields = ['student_id', 'user', 'last_modified_date']
#     success_url = '/class/add/'


# class AddStudent(FormView):
# template_name = 'edu/student_create.html'
# form_class = FormStudent
# success_url = '/class/add/'
# def form_valid(self, form):
#     form.save()
#     return super(AddStudent, self).form_valid(form)
