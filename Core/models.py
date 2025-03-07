from django.db import models

# Create your models here.
class Slider(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='slider')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    directs_to = models.URLField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    
class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, default='Customer')
    image = models.ImageField(upload_to='testimonial')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Banner(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='banner')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    offer_percent = models.CharField(max_length=10, default=0)
    directs_to = models.URLField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Contact Us"

    def __str__(self):
        return self.subject

class OurContact(models.Model):
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    street_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    building = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Our Contacts"
    
    
class WorkingHours(models.Model):
    monday_to_friday_opening_time = models.TimeField()
    monday_to_friday_closing_time = models.TimeField()
    saturday_opening_time = models.TimeField()
    saturday_closing_time = models.TimeField()

    class Meta:
        verbose_name_plural = "Working Hours"
    
class SocialMedia(models.Model):
    facebook = models.URLField()
    instagram = models.URLField()
    twitter = models.URLField()
    linkedin = models.URLField()
    youtube = models.URLField()
    
    class Meta:
        verbose_name_plural = "Social Media"
        
class Partner(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='partner')
    
class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team/')
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class NewsLetter(models.Model):
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email