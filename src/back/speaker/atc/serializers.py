from rest_framework import serializers
from .models import *

class CallTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallType
        fields =  '__all__'

class AvgSerializer(serializers.Serializer):
    avg = serializers.IntegerField()
    

    # def get_avg(self, obj):
    #     return  0 if obj['avg'] is None else obj['avg'].total_seconds()
class CountDPersonsSerializer(serializers.Serializer):
    persons=serializers.IntegerField()
    callsum = serializers.IntegerField()
class TopBaseSerializer(serializers.Serializer):    
    missed=serializers.IntegerField()
    dropped=serializers.IntegerField()
    
    total=serializers.IntegerField()
    
class District(serializers.Serializer):
    id = serializers.IntegerField(source='district')
    name = serializers.CharField(source='district__district_name')

class Regions(serializers.Serializer):
    id = serializers.IntegerField(source='ufns')    
    name = serializers.CharField(source='ufns__ufns_name')

class Tnos(serializers.Serializer):
    id = serializers.IntegerField(source='tno')
    region_id = serializers.IntegerField(source='ufns')  
    name = serializers.CharField(source='tno__tno_name')


class MapDistrictSerializer(District, TopBaseSerializer,CountDPersonsSerializer):
    dropped = serializers.IntegerField()
    

class MapRegionsSerializer(Regions, TopBaseSerializer,CountDPersonsSerializer):
    dropped = serializers.IntegerField()
    

class TopandavgDistrictSerializer(TopBaseSerializer,District, AvgSerializer,CountDPersonsSerializer): 
    dropped = serializers.IntegerField()   
    personsday=serializers.IntegerField()
    

class TopandavgRegionsSerializer(TopBaseSerializer,Regions, AvgSerializer,CountDPersonsSerializer):  
    dropped = serializers.IntegerField()  
    personsday=serializers.IntegerField()
    


class TopandavgTnosSerializer(TopBaseSerializer,Tnos, AvgSerializer,CountDPersonsSerializer): 
    dropped = serializers.IntegerField()   
    personsday=serializers.IntegerField()


class DynamicSerializer(serializers.Serializer):
    day = serializers.DateField(source='date_fixation')
    call_timedelta_avg = serializers.IntegerField()
    # def get_call_timedelta_avg(self, obj):
    #     return 0 if obj['call_timedelta_avg'] is None else obj['call_timedelta_avg'].total_seconds()

class MissedAccept(serializers.Serializer):
    missed = serializers.IntegerField()
    accepted = serializers.IntegerField()
    dropped = serializers.IntegerField()

class TotalDay(serializers.Serializer):
    day = serializers.DateField()    
    total=serializers.IntegerField()



class IncomemissedSerializer(MissedAccept,TotalDay):
    ...

class FunctionalitySerializer(TopBaseSerializer):
    id = serializers.IntegerField(source='depdirection')
    name=serializers.CharField(source='depdirection__name')



class RecallSerializer(TotalDay):
   
    recall = serializers.IntegerField()

class TimeclockerSerializer(MissedAccept):
    hour= serializers.IntegerField()




    

class DistrictSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    district_id = serializers.IntegerField(source ='subscriber_b__department__tno__ufns__district__id')
    district = serializers.CharField(source = 'subscriber_b__department__tno__ufns__district__district_name')
    region = serializers.IntegerField(source = "subscriber_b__department__tno__ufns__id")
    tno = serializers.IntegerField(source = "subscriber_b__department__tno__id")
    department=serializers.IntegerField(source = "subscriber_b__department__id")
    person = serializers.IntegerField(source ='subscriber_b__id')
    call_duration = serializers.IntegerField()
    time_fixation = serializers.DateTimeField()


class UfnsSerializer(DistrictSerializer):    
    ufns_id = serializers.IntegerField(source ='subscriber_b__department__tno__ufns__id')
    region = serializers.CharField(source = "subscriber_b__department__tno__ufns__ufns_name")
   

class TnoSerializer(UfnsSerializer):  
    tno_id = serializers.IntegerField(source ='subscriber_b__department__tno__id')        
    tno = serializers.CharField(source = "subscriber_b__department__tno__tno_name")
    
  

class DepSerializer(TnoSerializer):    
    deps_id = serializers.IntegerField(source ='subscriber_b__department__id')   
    department=serializers.CharField(source = "subscriber_b__department__deps_name")
    

class SubBSerializer(DepSerializer):    
    sub_b_id = serializers.IntegerField(source ='subscriber_b__id')   
    person = serializers.SerializerMethodField()
    disabled = serializers.BooleanField(source ='subscriber_b__disabled',allow_null=True)
    pwd_lastset = serializers.DateTimeField(source = 'subscriber_b__pwd_lastset',allow_null=True)
    
    def get_person(self,obj):
        return f"{obj['subscriber_b__given_name'] if len(obj['subscriber_b__given_name'])>0 else ''} {obj['subscriber_b__sn']}"