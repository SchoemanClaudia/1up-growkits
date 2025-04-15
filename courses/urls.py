from django.urls import path
from . import views

urlpatterns = [
    path('', views.online_courses, name='courses'),
    path('<int:course_id>', views.course_detail, name='course_detail'),
    path('add_course/', views.add_course, name='add_course'),
    path('edit_course/<int:course_id>/', views.edit_course, name='edit_course'),
    path('delete_course/<int:course_id>/', views.delete_course, name='delete_course'),
]