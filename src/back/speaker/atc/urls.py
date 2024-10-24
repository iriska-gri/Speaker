from django.urls import path
from .views import *

urlpatterns = [
  path('gettest/',TestInfo.as_view(),name='TestInfo' ),
  path('getinfo/', GetCallInfo.as_view(), name='GetCallInfo'),
  path('getdates/', GetCalldates.as_view(), name='GetCalldates'),
  path('getlevelinfo/', GetLevelInfo.as_view(), name="GetLevelInfo"),
  
]
