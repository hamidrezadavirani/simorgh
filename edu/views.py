from edu import forms
from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.list import ListView
from .models import Student, Classroom, Teacher, TeacherClassCourse, Register
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from .serializers import StudentSerializer, TeacherSerializer
from django.views.generic.edit import CreateView, UpdateView, DeleteView


class Register(CreateView):
    model = Register
    fields = '__all__'
    success_url = '/dashboard/'

class StudentListView(ListView):
    model = Student

    def get_context_data(self, **kwargs):
        context = super(StudentListView, self).get_context_data(**kwargs)
        form = forms.StudentSearchForm()
        context['form'] = form
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        first_name = self.request.GET.get('first_name')
        last_name = self.request.GET.get('last_name')

        if self.request.GET and any([first_name, last_name]):
            queryset = Student.objects.filter(
                Q(user__first_name=first_name) |
                Q(user__last_name=last_name)
            )
        return queryset


class StudentDeleteView(DeleteView):
    model = Student
    template_name_suffix = '_confirm_delete'
    success_url = '/students/'


class StudentCreateView(CreateView):
    model = Student
    fields = ['user', 'last_modified_date', 'student_id']
    success_url = '/students/'


class StudentUpdateView(UpdateView):
    model = Student
    fields = ['user', 'last_modified_date', 'student_id']
    success_url = '/students/'


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
        profession = self.request.GET.get('profession')
        education_degree = self.request.GET.get('education_degree')

        if self.request.GET and any([first_name, last_name, profession, education_degree]):
            queryset = Teacher.objects.filter(
                Q(user__first_name=first_name) |
                Q(user__last_name=last_name) |
                Q(education_degree=education_degree) |
                Q(profession__name=profession)
            )
        return queryset


class TeacherDeleteView(DeleteView):
    model = Teacher
    template_name_suffix = '_confirm_delete'
    success_url = ('/teachers/')


class TeacherCreateView(CreateView):
    model = Teacher
    success_url = '/teachers/'
    fields = '__all__'


class TeacherUpdateView(UpdateView):
    model = Teacher
    fields = '__all__'
    success_url = '/teachers/'


class TeacherClassCourseCreateView(CreateView):
    model = TeacherClassCourse
    fields = '__all__'
    success_url = '/dashboard/'


def about_us(request):
    return render(request, 'edu/about_us.html', {})


def contact_us(request):
    return render(request, 'edu/contact_us.html', {})


@login_required(login_url='/login/')
def display_dashboard(request):
    print(request.user.groups.all().first())
    return render(request, 'edu/dashboard.html', {})


def display_main(request):
    current_user = request.user
    # print(current_user)
    return render(request, 'edu/main.html', {})


def data_api(request):
    if request.method == 'GET':
        teachers = Teacher.objects.all()
        serialized = TeacherSerializer(teachers, many=True)
        data_dict = {'teachers': serialized.data}

        students = Student.objects.all()
        serialized = StudentSerializer(students, many=True)
        data_dict.update({'students': serialized.data})
        return JsonResponse(data_dict, safe=False)


class ClassroomListView(ListView):
    model = Classroom

    def get_context_data(self, **kwargs):
        context = super(ClassroomListView, self).get_context_data(**kwargs)
        form = forms.ClassroomSearchForm
        context['form'] = form
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        branch = self.request.GET.get('branch')
        education_year = self.request.GET.get('education_year')
        if self.request.GET and any([branch, education_year]):
            queryset = Classroom.objects.filter(Q(branch=branch) | Q(education_year=education_year))
        return queryset


class ClassroomDetailView(DetailView):
    model = Classroom
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context


def class_list(request, class_id):
    classroom = Classroom.objects.filter(id=class_id).first()
    classroom_students = list(Student.objects.filter(classroom=classroom))
    return render(request, 'edu/student_list.html', {'classroom_student': classroom_students})

# class AddStudent(FormView):
# template_name = 'edu/student_create.html'
# form_class = FormStudent
# success_url = '/class/add/'
# def form_valid(self, form):
#     form.save()
#     return super(AddStudent, self).form_valid(form)
