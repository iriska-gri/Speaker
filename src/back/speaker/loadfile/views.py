from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import *
import pandas as pd
from fns.models import *
from atc.models import *
from .serializers import *
import datetime
import requests
import json
import pytz
import os
import csv

import shutil
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
from .funcs import *
class UploadFileView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self,request):
        pass
class FakeAd(APIView):
    def post(self, request):
        p = os.path.join(settings.MEDIA_ROOT,'AD.csv')
        print(p)
        return FileResponse(open(p, "rb"))


class UPloadCallsAPIView(APIView):
    parser_classes = (MultiPartParser,)   

   
    @swagger_auto_schema(operation_description='Upload file...',
                         manual_parameters=[
                openapi.Parameter('login',openapi.IN_FORM, type=openapi.TYPE_STRING), 
                openapi.Parameter('password',openapi.IN_FORM, type=openapi.TYPE_STRING),           
                openapi.Parameter('file', openapi.IN_FORM, type=openapi.TYPE_ARRAY,
                                  items=openapi.Items(type=openapi.TYPE_FILE), description='Звонки'),
              
            ],
                         
                         )
    
    def post(self, request, **kwargs):
        # print(request.data['login'])
        print("****")
        set(pytz.all_timezones_set)  
        
        filesadd = request.FILES.getlist('file')
        # print(settings.MEDIA_ROOT)
        loadfolder = os.path.join(settings.MEDIA_ROOT,'uploads','loadcalls')
        print(loadfolder)
        if os.path.exists(loadfolder):
            shutil.rmtree(loadfolder)
        
        os.makedirs(loadfolder)
        fs = FileSystemStorage(location =loadfolder )
        filestoopen=[]

        for x in filesadd:
            filename = fs.save(x.name, x)
            filestoopen.append(filename)
        
        # resp= requests.post('http://10.252.44.13:8005/getAD', json.dumps({'user': self.username, 'password':self.password, 'usercheck': self.username}))   
        # resp= requests.post('http://127.0.0.1:8000/api/loadfile/fakead/', json.dumps({'user': request.data['login'], 'password':request.data['password'], 'usercheck': request.data['login']}), stream=True) 
        # res = None
        # if resp.status_code==200:
            
        #     with open(os.path.join(loadfolder,'AD.csv'), 'wb') as f:                
        #         resp.raw.decode_content = True
        #         shutil.copyfileobj(resp.raw, f) 
        #     adupdater(os.path.join(loadfolder,'AD.csv'))         
        # else:
        #     print(resp.status_code)            


        adload = AdLoader(filestoopen)
        adload.loadcalls()
        
            
        return Response ("ak")



class UPloadADAPIView(APIView):
    parser_classes = (MultiPartParser,)   

   
    @swagger_auto_schema(operation_description='Загрузка CSV AD...',
                         manual_parameters=[
                openapi.Parameter('file', openapi.IN_FORM, type=openapi.TYPE_FILE, description='Звонки'),
              
            ],
                         
                         )
    
    def post(self, request, **kwargs):
        
        filesadd = request.FILES.get('file')
        adupdater(filesadd)        
               
        return Response ("ak")

class DepsDirUploadView(APIView):
    # Django rest framework parser
    parser_classes = [MultiPartParser]
    
    # Нотация для swagger
    @swagger_auto_schema(
        operation_description='Загрузка файла...',
        manual_parameters=[openapi.Parameter('file', openapi.IN_FORM, type=openapi.TYPE_FILE, description='Обновление направлений отделов')],
        )
    
    # Загрузка файла с направлениями
    def post(self, request,*args,**kwargs):
           serializer = DepDirsUploadSerializer(data=request.data)

           if serializer.is_valid():
                file  = serializer.validated_data['file']

                file_data = file.read().decode('utf-8').splitlines()
                csv_reader = csv.reader(file_data)

                next(csv_reader, None)

                for row in csv_reader:
                    deps_name, depdirection_id = row[0], row[1]
                    Deps.objects.filter(deps_name = deps_name).update(depdirection_id = depdirection_id)
           return Response("ok")
                