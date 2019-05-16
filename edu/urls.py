from django.conf.urls import url
from edu import views


app_name = 'edu'

urlpatterns = [

    url(r'^(?P<class_id>[0-9])+/$', views.class_list),
    url(r'^students/$', views.StudentListView.as_view()),
    url(r'^students/create/$', views.StudentCreateView.as_view()),
    url(r'^studentsshow/$', views.students_show),
    url(r'^teachers/$', views.TeacherListView.as_view()),
    url(r'^teachers/create/$', views.TeacherCreateView.as_view()),
    url(r'^classrooms/$', views.ClassroomListView.as_view()),
    url(r'^classrooms/create/$', views.ClassroomCreateView.as_view()),
    url(r'^classrooms/(?P<pk>[0-9]+)/$',views.ClassroomDetailView.as_view()),
    url(r'^about_us/$', views.about_us),
    url(r'^contact_us/$', views.contact_us),
    url(r'^dashboard/$', views.display_dashboard),
    url('', views.display_main),


    # url(r'^add/(?P<pk>[0-9]+)/$', views.StudentUpdateView.as_view(), name='update'),
]




