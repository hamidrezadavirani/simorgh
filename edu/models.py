from django.db import models
from django.contrib.auth.models import User
import datetime


class Student(models.Model):
    student_id = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='students',
                                verbose_name='شماره دانش آموزی')
    courses = models.ManyToManyField('Course', through='StudentCourse', related_name='students')
    classrooms = models.ManyToManyField('Classroom', through='Register', related_name='students')
    last_modified_date = models.DateTimeField(null=True)
    birth_date = models.CharField(max_length=10, null=True)
    image = models.ImageField(upload_to='profile_image', blank=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hire_date = models.DateField()
    image = models.ImageField(upload_to='profile_image', blank=True)

    @property
    def get_experience(self):
        return datetime.datetime.now().year - self.hire_date.year

    DIPLOMA, ASSOCIATE, BACHELOR, MASTER, PHD = 'DP', 'AS', 'BA', 'MA', 'PHD'
    degree_choices = (
        (DIPLOMA, 'دیپلم'),
        (ASSOCIATE, 'فوق دیپلم'),
        (BACHELOR, 'لیسانس'),
        (MASTER, 'فوق لیسانس'),
        (PHD, 'دکتری')
    )
    education_degree = models.CharField(max_length=3, choices=degree_choices)
    profession = models.ManyToManyField('Course')

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class LevelField(models.Model):
    FIRST, SECOND, THIRD = 'first', 'second', 'third'
    level_choices = (
        (FIRST, 'اول'),
        (SECOND, 'دوم'),
        (THIRD, 'سوم')
    )

    level = models.CharField(max_length=10, choices=level_choices, default='first')
    MATH, NATURAL, HUMANITY = 'math', 'natural', 'humanity'
    field_choices = (
        (MATH, 'ریاضی'),
        (NATURAL, 'تجربی'),
        (HUMANITY, 'انسانی')
    )
    field = models.CharField(max_length=10, choices=field_choices)

    def __str__(self):
        return self.get_level_display() + ' ' + self.get_field_display()


class Classroom(models.Model):
    level_field = models.ForeignKey('LevelField', on_delete=models.SET_NULL, null=True, related_name='classrooms')
    A, B, C = 'a', 'b', 'c'
    branch_choices = (
        (A, 'الف'),
        (B, 'ب'),
        (C, 'ج')
    )

    branch = models.CharField(max_length=1, choices=branch_choices, null=True)
    education_year = models.CharField(max_length=20, null=True)
    courses = models.ManyToManyField('Course', through='TeacherClassCourse', related_name='classrooms')
    teachers = models.ManyToManyField('Teacher', through='TeacherClassCourse', related_name='classrooms')

    def __str__(self):
        return str(self.level_field) + ' ' + self.get_branch_display()


class Course(models.Model):
    name = models.CharField(max_length=20)
    level_field = models.ForeignKey('LevelField', on_delete=models.SET_NULL, null=True, related_name='courses')
    unit = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class StudentCourse(models.Model):
    student = models.ForeignKey('Student', related_name='student_courses', on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey('Course', related_name='student_courses', on_delete=models.SET_NULL, null=True)
    final_grade = models.FloatField(null=True)
    mid_grade = models.FloatField(null=True)


class Register(models.Model):
    student = models.ForeignKey('Student', related_name='registers', on_delete=models.SET_NULL, null=True)
    classroom = models.ForeignKey('Classroom', related_name='registers', on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField()

    def __str__(self):
        return str(self.student) + ' ' + str(self.classroom)


class TeacherClassCourse(models.Model):
    teacher = models.ForeignKey('Teacher', related_name='teacher_class_courses', on_delete=models.SET_NULL, null=True)
    classroom = models.ForeignKey('Classroom', related_name='teacher_class_courses', on_delete=models.SET_NULL,
                                  null=True)
    course = models.ForeignKey('Course', related_name='teacher_class_courses', on_delete=models.SET_NULL, null=True)
    class_time = models.DateTimeField()

    def __str__(self):
        return str(self.teacher) + ' ' + str(self.classroom) + ' ' + str(self.course)
