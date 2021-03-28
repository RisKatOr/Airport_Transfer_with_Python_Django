from django.contrib import admin

# Register your models here.
from home.models import Setting, ContactFormMessage


class ContactformMessageAdmin(admin.ModelAdmin):
    list_display = ['name','subject','note','status']
    list_filter = ['status']

admin.site.register(ContactFormMessage,ContactformMessageAdmin)
admin.site.register(Setting)