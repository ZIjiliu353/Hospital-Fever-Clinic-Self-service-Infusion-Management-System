from django.urls import path
from . import views

urlpatterns = [
    path('medication_list/', views.medication_list, name='medication_list'),
    path('add_medication_api/', views.add_medication_api, name='add_medication_api'),
    path('edit_medication/', views.edit_medication, name='edit_medication'),
    path('delete_medication/<int:medication_id>/', views.delete_medication, name='delete_medication'),
]

