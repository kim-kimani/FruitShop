from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about-us', views.about_us, name='about_us'),
    path('newsletter', views.newsletter, name='newsletter'),
    path('contact-us', views.contact_us, name='contact_us'),
]