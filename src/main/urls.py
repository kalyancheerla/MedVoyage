from django.urls import path
from . import views

urlpatterns = [

    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.user_login, name="user_login"),
    path("about/", views.about_us, name="about_us"),
    path("contact/", views.contact_us, name="contact_us"),
    path("signout/", views.signout, name="signout"),
    path("reset_password/", views.reset_password, name='reset_password'),
    path("client_dashboard/",views.client_dashboard, name='client_dashboard'),
    path('client_profile/', views.client_profile, name='client_profile'),
    path('client_update/', views.update_patient_info, name='update_patient_info'),
    path("doctor_dashboard/",views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor_profile/', views.doctor_profile, name='doctor_profile'),
    path('doctor_update/', views.update_doctor_info, name='update_doctor_info'),
    path('verification/', views.verification, name='verification'),
    path('client_appointments/', views.patient_appointments, name='patient_appointments'),
    path('add_slots/', views.add_slots, name = 'add_slots'),
    path('slots/', views.slots_list, name='slots_list'),
    path('slots/edit/<int:slot_id>/', views.edit_slot, name='edit_slot'),
    path('slots/delete/<int:slot_id>/', views.delete_slot, name='delete_slot'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('get-doctor-availability-hours/', views.get_doctor_availability_hours, name='get_doctor_availability_hours'),

]
