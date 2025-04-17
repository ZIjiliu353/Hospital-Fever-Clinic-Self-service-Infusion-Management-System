from django.urls import path
from . import views

urlpatterns = [
    path('patient_infusion/', views.patient_infusion, name='patient_infusion'),
    path('get_patient_infusion/', views.get_patient_infusion, name='get_patient_infusion'),
    path('updateCheckInStatus/<int:infusion_id>/', views.updateCheckInStatus, name='updateCheckInStatus'),
    path('updateSitDownStatus/<int:infusion_id>/', views.updateSitDownStatus, name='updateSitDownStatus'),
    path('nurse_infusion/', views.nurse_infusion, name='nurse_infusion'),
    path('get_nurse_infusion/', views.get_nurse_infusion, name='get_nurse_infusion'),
    path('updateGetMedicationAndInfusionStatus/<int:infusion_id>/', views.updateGetMedicationAndInfusionStatus, name='updateGetMedicationAndInfusionStatus'),
    path('updateCompleteStatus/<int:infusion_id>/', views.updateCompleteStatus, name='updateCompleteStatus'),
    path('updateRemoveNeedleStatus/<int:infusion_id>/', views.updateRemoveNeedleStatus,name='updateRemoveNeedleStatus'),
    path('nurse_infusion_history/', views.nurse_infusion_history, name='nurse_infusion_history'),
    path('get_nurse_infusion_history/', views.get_nurse_infusion_history, name='get_nurse_infusion_history'),
    path('updateCancelStatus/<int:infusion_id>/', views.updateCancelStatus, name='updateCancelStatus'),
    path('patient_updateCancelStatus/<int:infusion_id>/', views.patient_updateCancelStatus, name='patient_updateCancelStatus'),
]
