from django.urls import path
from . import views 


urlpatterns = [
    path('', views.home, name='home'),
    path('patient/', views.patient, name='patient'),
    path('register/', views.register_patient, name='register_patient'),
    path('login/', views.login_patient, name='login_patient'),
    path('p_register/', views.p_register, name='p_register'),  # Ajout de l'URL pour p_register
    path('doctor_signup/', views.doctor_signup, name='doctor_signup'),
    path('doctor_login/', views.doctor_login, name='doctor_login'),
    path('doctor/', views.doctor, name='doctor'),
    path('search_doctors/', views.search_doctors, name='search_doctors'),
    path('book_appointment/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('manage_appointments/', views.manage_appointments, name='manage_appointments'),
    path('update_appointment_status/<int:appointment_id>/', views.update_appointment_status, name='update_appointment_status'),
    path('patient/', views.patient, name='patient'),
    path('change_password/', views.change_password, name='change_password'),
    path('doctor_change_password/', views.doctor_change_password, name='doctor_change_password'),
    path('medintroduction/', views.medintroduction, name='medintroduction'),

   
]
