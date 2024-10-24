from django.urls import path
from .views import *


urlpatterns = [
    path('filter/', Filter.as_view(), name='filter'),
    path('getdepartments/', GetDepartments.as_view(), name='getdepartments'),
    path('getdirections/', GetDirections.as_view(), name='getdirections'),

]
