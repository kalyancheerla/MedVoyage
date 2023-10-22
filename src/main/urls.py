from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about_us, name="about_us"),
    path("contact/", views.contact_us, name="contact_us"),
    path('contact/submit/', views.contact_us_form_submit, name='contact_us_form_submit'),
]
