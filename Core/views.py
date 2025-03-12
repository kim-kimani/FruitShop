from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import threading
from django.shortcuts import render, redirect
from .models import Testimonial, SocialMedia, WorkingHours, Banner, OurContact, Partner, TeamMember, NewsLetter, ContactUs

# Create your views here.
def index(request):
    our_contact = OurContact.objects.first()
    working_hours = WorkingHours.objects.first()
    testimonials = Testimonial.objects.filter(is_active=True).order_by('-created_at')
    
    context = {
        'our_contact': our_contact,
        'working_hours': working_hours,
        'testimonials': testimonials
    }
    return render(request, 'index.html', context)

def about_us(request):
    working_hours = WorkingHours.objects.first()
    testimonials = Testimonial.objects.filter(is_active=True).order_by('-created_at')
    social_media = SocialMedia.objects.all()
    banner = Banner.objects.filter(is_active=True).order_by('-created_at').first()
    our_contact = OurContact.objects.first()
    partners = Partner.objects.all()
    team_members = TeamMember.objects.filter(is_active=True)
    
    context = {
        'working_hours': working_hours,
        'testimonials': testimonials,
        'social_media': social_media,
        'banner': banner,
        'our_contact': our_contact,
        'partners': partners,
        'team_members': team_members,
    }
    
    return render(request, 'aboutus.html', context)


def newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                NewsLetter.objects.create(email=email)
            except Exception as e:
                pass
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    return render(request, request.path)

def send_email_in_thread(name, email, message):
    html = render_to_string('email.html', {
        'name': name,
        'message': message
    })
    
    email = EmailMessage(
        subject='We have received your message',
        body=html,
        from_email='"Hapa254 Kenya Ltd" <{}>'.format(settings.EMAIL_HOST_USER),
        to=[email],
    )
    
    email.content_subtype = "html"
    email.send(fail_silently=False)
    print('Email sent')
    
def contact_us(request):
    our_contact = OurContact.objects.first()
    working_hours = WorkingHours.objects.first()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        ContactUs.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,            
            message=message,
        )

        # Send the email in a separate thread, Page reloads, email sends in background
        email_thread = threading.Thread(
            target=send_email_in_thread,
            args=(name, email, message)
        )
        email_thread.start()
                
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    context = {
        'our_contact': our_contact,
        'working_hours': working_hours,
    }
    
    return render(request, 'contact_us.html', context )