from django.urls import path
from .views import *


urlpatterns = [
    path('', UploadFileView.as_view(), name='loadfile'),
    path('uploadcalls/', UPloadCallsAPIView.as_view(), name='upcal'),
    path('uploadad/', UPloadADAPIView.as_view(), name='apad'),
    path ('depsdirupload/', DepsDirUploadView.as_view(), name='deps_dirs_upload'),  
    path('fakead/',FakeAd.as_view(), name='FakeAd'),

]
