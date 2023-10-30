from django.contrib import admin
from .models import CarMake, CarModel
# from .models import related models


# Register your models here.

class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 3  # You can change the number of empty forms to display

class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'dealer_id', 'car_type', 'year')
    list_filter = ('car_make', 'car_type', 'year')
    search_fields = ('name', 'car_make__name', 'dealer_id')
    list_select_related = ('car_make',)  # Optimize database queries by selecting the related CarMake
    list_per_page = 20  # Set the number of items per page in the admin list view
    ordering = ('-year', 'car_make__name', 'name')  # Default ordering for the list view
    # Other options can be customized according to your needs



class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]

# Register the models and the admin classes
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
# Register models here
