from django.contrib import admin

# Register your models here.
from reservation.models import ShopCart


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'car', 'from_location', 'to_location', 'calculated_price']
    list_filter =  ['user']



admin.site.register(ShopCart,ShopCartAdmin)

