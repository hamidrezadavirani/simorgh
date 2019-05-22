from django.conf.urls import url
from edu import views


app_name = 'edu'

urlpatterns = [


    url(r'^data_api/$', views.data_api),

    url(r'^teachers/create/$', views.TeacherCreateView.as_view()),
    url(r'^teachers/$', views.TeacherListView.as_view()),
    url(r'^teachers/update/(?P<pk>[0-9]+)/$', views.TeacherUpdateView.as_view()),
    url(r'^teachers/delete/(?P<pk>[0-9]+)/$', views.TeacherDeleteView.as_view()),

    url(r'^students/create/$', views.StudentCreateView.as_view()),
    url(r'^students/$', views.StudentListView.as_view()),
    url(r'^students/update/(?P<pk>[0-9]+)/$', views.StudentUpdateView.as_view()),
    url(r'^students/delete/(?P<pk>[0-9]+)/$', views.StudentDeleteView.as_view()),

    url(r'^teacherclasscourse/$', views.TeacherClassCourseCreateView.as_view()),

    url(r'^classrooms/$', views.ClassroomListView.as_view()),
    url(r'^classrooms/(?P<pk>[0-9]+)/$',views.ClassroomDetailView.as_view()),

    url(r'^register/$' , views.Register.as_view()),

    url(r'^about_us/$', views.about_us),
    url(r'^contact_us/$', views.contact_us),
    url(r'^dashboard/$', views.display_dashboard),
    url(r'^$', views.display_main),
    # url(r'^(?P<class_id>[0-9])+/$', views.class_list),
    # url(r'^add/(?P<pk>[0-9]+)/$', views.StudentUpdateView.as_view(), name='update'),
]




