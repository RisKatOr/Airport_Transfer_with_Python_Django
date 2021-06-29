from django.contrib import admin

# Register your models here.
from reservation.models import ShopCart


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'car', 'from_location', 'to_location', 'calculated_price']
    list_filter =  ['user']

class ReserveAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'from_location','phone', 'to_location', 'status']
    list_filter = ['status']
    readonly_fields = ('user','address','phone','first_name','last_name','ip')
    # inlines = [ReserveCarline]

class ReserveCarAdmin(admin.ModelAdmin):
    list_display = ['user','car','price']
    list_filter = ['user']

admin.site.register(ShopCart,ShopCartAdmin)

