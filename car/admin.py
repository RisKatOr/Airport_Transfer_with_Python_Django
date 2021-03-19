from django.contrib import admin
from car.models import Category, Car


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['status']
    # fields = ['title', 'status']
    # field sadece ekleme silme düzenleme gibi durumlarda dikkate alınacak değişkenleri belirler

admin.site.register(Category,CategoryAdmin)
class CarAdmin(admin.ModelAdmin):
    list_display = ['title','category', 'status']
    list_filter = ['status','category']
admin.site.register(Car,CarAdmin)
