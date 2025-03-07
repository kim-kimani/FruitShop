from django.contrib import admin
from .models import Slider, NewsLetter, Testimonial, Banner, ContactUs, OurContact, WorkingHours, SocialMedia, TeamMember, Partner

# Register your models here.
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at', 'directs_to', 'is_active')
    
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'is_active')
    
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at', 'is_active')
    
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'message', 'created_at')
    
class OurContactAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email', 'street_name', 'city', 'state', 'building')
    
class WorkingHoursAdmin(admin.ModelAdmin):
    list_display = ('monday_to_friday_opening_time', 'monday_to_friday_closing_time', 'saturday_opening_time', 'saturday_closing_time')
    
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ('facebook', 'instagram', 'twitter', 'linkedin', 'youtube')
    
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'is_active')

class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')

admin.site.register(Slider, SliderAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(OurContact, OurContactAdmin)
admin.site.register(WorkingHours, WorkingHoursAdmin)    
admin.site.register(SocialMedia, SocialMediaAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(Partner)
admin.site.register(NewsLetter, NewsLetterAdmin)