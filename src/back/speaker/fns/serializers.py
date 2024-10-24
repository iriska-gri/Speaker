from rest_framework import serializers
from .models import *


class DistrictSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source = 'district_name')
    code = serializers.CharField(source = 'district_code')
    class Meta:
        fields = ['id', 'name', 'code']
        model = District


class UfnsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source = 'ufns_name')
    code = serializers.CharField(source = 'ufns_code')
    parent = serializers.IntegerField(source='district_id')
    class Meta:
        fields = ['id', 'name', 'code','parent']
        model = Ufns


class TnoSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='tno_name')
    code = serializers.CharField(source='tno_code')
    parent = serializers.IntegerField(source='ufns_id')
    parent__parent = serializers.IntegerField(source='ufns.district_id')
    class Meta:
        fields = ['id', 'name', 'code','parent','parent__parent']
        model = Tno

class DepartmentSerializer(serializers.ModelSerializer):
    name=serializers.CharField(source='deps_name')
    # parent = serializers.IntegerField(source='tno_id')

    class Meta:
        fields = ['id', 'name','depdirection']
        model = Deps

class DepsDirectionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = DepDirection

class AdFilterSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    parent = serializers.IntegerField(source='department_id')
    disabled = serializers.BooleanField()
    
    def get_name(self, obj):
        return f'{obj.sn} {obj.given_name}'
    
    class Meta:
        fields = ['id', 'name', 'parent', 'disabled']
        model = Ad