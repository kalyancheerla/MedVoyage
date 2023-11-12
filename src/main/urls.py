from django.urls import path
from . import views

urlpatterns = [
    
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.user_login, name="user_login"),
    path("about/", views.about_us, name="about_us"),
    path("contact/", views.contact_us, name="contact_us"),
    path('contact/submit/', views.contact_us_form_submit, name='contact_us_form_submit'),
    path("signout/", views.signout, name="signout"),
    path("reset_password/", views.reset_password, name='reset_password'),
    path("book_appointment/", views.book_appointment, name='book_appointment'),
    path("client_dashboard/",views.client_dashboard, name='client_dashboard'),
    path('client_profile/', views.client_profile, name='client_profile'),
    path('client_update/', views.update_patient_info, name='update_patient_info'),
    path("cancel_appointment/", views.cancel_appointment, name='cancel_appointment'),
    path("view_schedule/", views.view_schedule, name='view_schedule'),
]
