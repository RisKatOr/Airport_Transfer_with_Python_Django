from django.contrib import admin
from car.models import Category, Car, Images, Comment
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin


# Register your models here.

class CarImageInline(admin.TabularInline):
    model = Images
    extra = 5

class CategoryAdmin(MPTTModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['status']
    # fields = ['title', 'status']
    # field sadece ekleme silme düzenleme gibi durumlarda dikkate alınacak değişkenleri belirler

class CarAdmin(admin.ModelAdmin):
    list_display = ['title','category','image_tag', 'status']
    readonly_fields = ('image_tag',)
    list_filter = ['status','category']
    inlines =  [CarImageInline]

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title','car']
    list_filter = ['car']



class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Car,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Car,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'



class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject','comment', 'car','user','status']
    list_filter = ['status']


admin.site.register(Comment,CommentAdmin)
admin.site.register(Category,CategoryAdmin2)
admin.site.register(Images,ImagesAdmin)
admin.site.register(Car,CarAdmin)