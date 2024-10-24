from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from .models import *
from atc.models import *
from atc.serializers import *
from .serializers import *
import pandas as pd
from django.http import HttpResponse

# Основной и единственный приемник ключей от фильтров с фронтэнда
class Filter(APIView):
    def get(self, request):  
        # Чистые фильтры без фильтрации
        try:
            
            return Response(getattr(self, self.request.GET.get('q', 'empty'))())
        # Условия для работы с ключами фильтра    
        except Exception as e:
            print(e)
            return Response({'error': 'str(e)'})



    def district(self):
        return   DistrictSerializer(District.objects.all().order_by('district_code'), many=True).data
    
    def regions(self):
        return UfnsSerializer(Ufns.objects.all().order_by('ufns_code'), many=True).data
    
    def call_type(self):
        return CallTypeSerializer(CallType.objects.all(), many=True).data
    
    def tno(self):
        return TnoSerializer(Tno.objects.all().order_by('tno_code'), many=True).data
    
    def department(self):
        return DepartmentSerializer(Deps.objects.all(), many=True).data

    def direction(self):
        return DepsDirectionSerializer(DepDirection.objects.all(),many=True).data

    def person(self):
        return AdFilterSerializer(Ad.objects.all().order_by('sn'), many=True).data

    def empty(self):
        return {'message':"Пустой или неверный параметр"}

class GetDepartments(APIView):
    def get(self,request):
        queryset = DepartmentSerializer(Deps.objects.all().distinct("deps_name"),many=True).data
        deps_and_id = pd.DataFrame(queryset).sort_values("id")
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=deps_and_dir_id.csv'
        deps_and_id.to_csv(path_or_buf=response, index=False, sep = ';', columns=["name","depdirection"])
        return response
        
class GetDirections(APIView):
    def get(self,request):
        queryset = DepsDirectionSerializer(DepDirection.objects.all().distinct("name"),many=True).data
        direct_and_id = pd.DataFrame(queryset).sort_values("id")
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=directs_and_id.csv'
        direct_and_id.to_csv(path_or_buf=response, index=False, sep = ';', columns=["id","name"])
        return response