from django.contrib import admin
from .models import *

admin.site.register(CallType)
admin.site.register(CallCauses)
admin.site.register(Sources)
# admin.site.register(Calls)

class YourModelAdmin(admin.ModelAdmin): 
    change_form_template = 'admin/atc/change_list.html'


