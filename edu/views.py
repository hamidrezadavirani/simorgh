from edu import forms
from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import Group
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Student, Classroom, Teacher, TeacherClassCourse, Register, StudentCourse, User
from .serializers import StudentSerializer, TeacherSerializer, RegisterSerializer
from django.contrib.auth.hashers import make_password
from django.forms.models import model_to_dict

staff_group = user_passes_test(lambda u: any([
    Group.objects.get(name='staff') in u.groups.all()
]))

teacher_group = user_passes_test(lambda u: any([
    Group.objects.get(name='staff') in u.groups.all(),
    Group.objects.get(name='teacher') in u.groups.all()
]))

student_group = user_passes_test(lambda u: any([
    Group.objects.get(name='staff') in u.groups.all(),
    Group.objects.get(name='teacher') in u.groups.all(),
    Group.objects.get(name='student') in u.groups.all()
]))


class Register(CreateView):
    success_url = '/dashboard/'
    form_class = forms.RegisterForm
    template_name = 'edu/register_form.html'

    def form_valid(self, form):
        form.save()
        for course in list(form.cleaned_data['classroom'].courses.all()):
            StudentCourse.objects.get_or_create(student=form.cleaned_data['student'], course=course)
        return super().form_valid(form)


@method_decorator(staff_group, name='dispatch')
class StudentListView(ListView):
    model = Student

    def get_context_data(self, **kwargs):
        context = super(StudentListView, self).get_context_data(**kwargs)
        form = forms.StudentSearchForm()
        context['form'] = form
        students = Student.objects.all()
        fields = []
        for student in students:
            register_entry = student.registers.first()
            try:
                level_field = register_entry.classroom.level_field.get_field_display()
                fields.append(level_field)
            except:
                fields.append('ثبت نام نشده')

        context['fields'] = fields
        return context

    def dispatch(self, request, *args, **kwargs):
        return super(StudentListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()

        first_name = self.request.GET.get('first_name')
        last_name = self.request.GET.get('last_name')
        birth_date = self.request.GET.get('birth_date')
        field = self.request.GET.get('field')
        level = self.request.GET.get('level')

        if self.request.GET and any([first_name, last_name, birth_date, field, level]):
            queryset = Student.objects.filter(
                Q(user__first_name=first_name) |
                Q(user__last_name=last_name) |
                Q(birth_date=birth_date) |
                Q(classrooms__level_field__field=field) |
                Q(classrooms__level_field__level=level)
            )
        print(queryset)
        return queryset


@method_decorator(staff_group, name='dispatch')
class StudentDeleteView(DeleteView):
    model = Student
    template_name_suffix = '_confirm_delete'
    success_url = '/students/'

    def delete(self, request, *args, **kwargs):
        print('i deleted this bastard')
        return super(StudentDeleteView, self).delete(self, request, *args, **kwargs)


@method_decorator(staff_group, name='dispatch')
class StudentCreateView(CreateView):
    model = Student
    success_url = '/students/'
    form_class = forms.StudentCreateViewForm

    def form_valid(self, form):
        usr = User.objects.create(username=form.cleaned_data.pop('username'),
                                  first_name=form.cleaned_data.pop('first_name'),
                                  last_name=form.cleaned_data.pop('last_name'),
                                  password=make_password(form.cleaned_data.pop('password')),
                                  )

        std = form.save(commit=False)

        std.user = usr
        std.id = form.cleaned_data['student_id']
        std.birth_date = form.cleaned_data['birth_date']
        std.image = form.cleaned_data['image']
        std.save()

        group = Group.objects.get(name='student')

        group.user_set.add(std.user)
        group.save()

        return super(StudentCreateView, self).form_valid(form)


@method_decorator(staff_group, name='dispatch')
class StudentUpdateView(UpdateView):
    model = Student
    success_url = '/students/'
    form_class = forms.StudentCreateViewForm

    def get_initial(self):
        self.initial.update(model_to_dict(User.objects.filter(students__student_id=self.object.pk).first()
                                          , fields=['first_name', 'last_name', 'username', 'password']))
        return self.initial.copy()

    def form_valid(self, form):
        User.objects.filter(students__student_id=self.object.pk).update(
            username=form.cleaned_data.pop('username'),
            first_name=form.cleaned_data.pop('first_name'),
            last_name=form.cleaned_data.pop('last_name'),
            password=make_password(form.cleaned_data.pop('password')),

        )

        return super(StudentUpdateView, self).form_valid(form)


@method_decorator(staff_group, name='dispatch')
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


@method_decorator(staff_group, name='dispatch')
class TeacherDeleteView(DeleteView):
    model = Teacher
    template_name_suffix = '_confirm_delete'
    success_url = ('/teachers/')


@method_decorator(staff_group, name='dispatch')
class TeacherCreateView(CreateView):
    model = Teacher
    success_url = '/teachers/'
    fields = '__all__'

    def get_queryset(self):
        if str(self.request.user.groups.first()) == 'teacher':
            self.query_set = super().get_queryset()
        else:
            self.queryset = None
        return self.request


@method_decorator(staff_group, name='dispatch')
class TeacherUpdateView(UpdateView):
    model = Teacher
    fields = '__all__'
    success_url = '/teachers/'

    # we can control access by:
    #     1. permission in django admin using groups
    #     2. access view using dispatch (better to do with decorator) (if use has_perm in dispatch actually we are using option 1 )
    #     3. using queryset (lets users to request to view and then get the queryset)

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.has_perm('eud.change_teacher'):
    #         return super(TeacherUpdateView, self).dispatch(request,*args,**kwargs)
    #     else:
    #         return render(request, 'edu/404.html',{})

    # we can also use this shit but again it calls the get_queryset
    # def get_object(self, queryset=None):
    #     pass


@method_decorator(staff_group, name='dispatch')
class TeacherClassCourseCreateView(CreateView):
    model = TeacherClassCourse
    fields = '__all__'
    success_url = '/dashboard/'


def about_us(request):
    return render(request, 'edu/about_us.html', {})


def p404(request, exception):
    return render(request, '404.html', {})


def contact_us(request):
    return render(request, 'edu/contact_us.html', {})


@login_required(login_url='/login/')
def display_dashboard(request):
    return render(request, 'edu/dashboard.html', {})


def display_main(request):
    current_user = request.user
    return render(request, 'edu/main.html', {})


def data_api(request):
    if request.method == 'GET':
        teachers = Teacher.objects.all()
        serialized = TeacherSerializer(teachers, many=True)
        data_dict = {'teachers': serialized.data}

        students = Student.objects.all()
        serialized = StudentSerializer(students, many=True)
        data_dict.update({'students': serialized.data})

        registers = Register.objects.all()
        serialized = RegisterSerializer(registers, many=True)
        data_dict.update({'registers': serialized.data})

        return JsonResponse(data_dict, safe=False)


@method_decorator(student_group, name='dispatch')
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


@method_decorator(student_group, name='dispatch')
class ClassroomDetailView(DetailView):
    model = Classroom
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# def class_list(request, class_id):
#     classroom = Classroom.objects.filter(id=class_id).first()
#     classroom_students = list(Student.objects.filter(classroom=classroom))
#     return render(request, 'edu/student_list.html', {'classroom_student': classroom_students})


# class AddStudent(FormView):
# template_name = 'edu/student_create.html'
# form_class = FormStudent
# success_url = '/class/add/'
# def form_valid(self, form):
#     form.save()
#     return super(AddStudent, self).form_valid(form)
