from django.contrib import admin
from .models import *

admin.site.register(District)
admin.site.register(Ufns)
admin.site.register(Tno)
admin.site.register(HolidayExculisions)

class DepsAdmin(admin.ModelAdmin):
    list_display = ('deps_name', 'tno', 'depdirection')
    search_fields = ['deps_name', 'depdirection__name']
admin.site.register(Deps, DepsAdmin)

class DepDirectionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']
admin.site.register(DepDirection,DepDirectionAdmin)

admin.site.register(Ad)
