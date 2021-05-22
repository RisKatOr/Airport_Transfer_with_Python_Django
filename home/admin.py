from django.contrib import admin

# Register your models here.
from home.models import Setting, ContactFormMessage, UserProfile


class ContactformMessageAdmin(admin.ModelAdmin):
    list_display = ['name','subject','note','status']
    list_filter = ['status']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['image_tag','first_name','user_name', 'country']


admin.site.register(ContactFormMessage,ContactformMessageAdmin)
admin.site.register(Setting)
admin.site.register(UserProfile,UserProfileAdmin)