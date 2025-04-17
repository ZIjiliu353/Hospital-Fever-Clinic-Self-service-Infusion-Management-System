from user import views
from django.urls import path

urlpatterns = [
    path('home/login/', views.home, name="home"),
    path('doctor/login/', views.doctor_login, name='doctor_login'),
    path('nurse/login/', views.nurse_login, name='nurse_login'),
    path('patient/login/', views.patient_login, name='patient_login'),
    path('doctor/register/', views.doctor_register, name='doctor_register'),
    path('nurse/register/', views.nurse_register, name='nurse_register'),
    path('patient/register/', views.patient_register, name='patient_register'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('nurse_dashboard/', views.nurse_dashboard, name='nurse_dashboard'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor_dashboard/profile/', views.doctor_profile, name='doctor_profile'),
    path('doctor_dashboard/edit_profile/', views.doctor_edit_profile, name='doctor_edit_profile'),
    path('nurse_dashboard/profile/', views.nurse_profile, name='nurse_profile'),
    path('nurse_dashboard/edit_profile/', views.nurse_edit_profile, name='nurse_edit_profile'),
    path('patient_dashboard/profile/', views.patient_profile, name='patient_profile'),
    path('patient_dashboard/edit_profile/', views.patient_edit_profile, name='patient_edit_profile'),
    path('patient_dashboard/doctor_list/', views.patient_doctor_list, name='patient_doctor_list'),
    path('doctor_detail/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
]


