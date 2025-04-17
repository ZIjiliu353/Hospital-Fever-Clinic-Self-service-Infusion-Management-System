from django.urls import path
from . import views

urlpatterns = [
    path('make_patient_appointment/', views.make_patient_appointment, name='make_patient_appointment'),
    path('get_doctors/', views.get_doctors, name='get_doctors'),
    path('get_doctor_balance/', views.get_doctor_balance, name='get_doctor_balance'),
    path('submit_appointment/', views.submit_appointment, name='submit_appointment'),
    path('view_appointment_history/', views.view_appointment_history, name='view_appointment_history'),
    path('get_appointment_data/', views.get_appointment_data, name='get_appointment_data'),
    path('appointment_handling/', views.appointment_handling, name='appointment_handling'),
    path('doctor_get_appointment_data/', views.doctor_get_appointment_data, name='doctor_get_appointment_data'),
    path('get_medications/', views.get_medications, name='get_medications'),
    path('doctor_deal_with_appointment/', views.doctor_deal_with_appointment, name='doctor_deal_with_appointment'),
    path('patient_detail/', views.patient_detail, name='patient_detail'),
]
