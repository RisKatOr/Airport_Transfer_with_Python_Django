from django.contrib import admin
from car.models import Category, Car, Images


# Register your models here.

class CarImageInline(admin.TabularInline):
    model = Images
    extra = 5

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['status']
    # fields = ['title', 'status']
    # field sadece ekleme silme düzenleme gibi durumlarda dikkate alınacak değişkenleri belirler

class CarAdmin(admin.ModelAdmin):
    list_display = ['title','category', 'status']
    list_filter = ['status','category']
    inlines =  [CarImageInline]

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title','car']
    list_filter = ['car']




admin.site.register(Category,CategoryAdmin)
admin.site.register(Images,ImagesAdmin)
admin.site.register(Car,CarAdmin)