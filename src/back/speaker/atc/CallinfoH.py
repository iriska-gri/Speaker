import pandas as pd
from django.db.models import Avg, Min, Max, Sum, Count,Q,F,ExpressionWrapper, Value, Func
import asyncio
from asgiref.sync import sync_to_async
from .models import *
from .serializers import *

class CallinfoCalculator:
    """
    Класс-обработчик и счетовод
    """

    def __init__(self):
        ...

    def persons_personsday_counter(self,a,b):
        for x in a:            
            try:             
                x['persons']=sum([xb['persons'] for xb in [el for el in b if el[self.idval]==x[self.idval]]])
                
                              
              
            except Exception:
                pass 
        return a
    




class CallinfoHqueryBuildier:
    """
    Вспомогательный класс для построения запросов и сериализации данных.\
    Формирует: -фильтры
               - сериализаторы
               - values
               
    """
    def __init__(self):
        ...
    
    
    async def getvalandfilters(self, filters):
        self.val = ''
        self.idval=''
        k=''
        if self.funct=='previoustopavg':
            filters['date_fixation__gte']=filters['pdate_fixation__gte']
            filters['date_fixation__lte']=filters['pdate_fixation__lte']
        del filters['pdate_fixation__gte']
        del filters['pdate_fixation__lte']
        

        
        if filters['mapscale']==1:
            # округа
            self.val = ['district','district__district_name']
            self.idval='district'
            self.to_serializer = 'district'
            pass
            if 'district' in filters.keys():
                self.to_serializer = 'regions'
                filters['district__in']=filters['district']
                self.val = ['ufns','ufns__ufns_name']
                self.idval='ufns'
                del filters['district']
            
        else:
            self.to_serializer = 'regions'
            self.val = ['ufns','ufns__ufns_name']
            self.idval='ufns'
            if 'regions' in filters.keys():
                if self.funct!='maprussia':
                    self.to_serializer = 'tnos' 
                    self.val = ['ufns','tno','tno__tno_name']                
                    self.idval='tno'
                filters['ufns__in']=filters['regions']
                del filters['regions']
        
        del filters['mapscale']


        # if 'call_duration' in filters.keys():
        #     filters['call_duration']=datetime.timedelta(seconds=filters['call_duration'])
        # elif 'call_duration__gt' in filters.keys():
        #     filters['call_duration__gt']=datetime.timedelta(seconds=filters['call_duration__gt'])
        
        if 'call_time_msc' in filters.keys():          
            if filters['call_time_msc']==1:
                
                self.filters2.append(Q(wt=True))
              
            else:
                self.filters2.append( Q(wt=False))
                
            del filters['call_time_msc']
        if 'holiday' in filters.keys():
          
            hh={'workexception':[],
                'holexception':[],
                }
          
            if filters['holiday'] is not None:
                holidays = await sync_to_async(list)(HolidayExculisions.objects.filter(holiday_date__gte=filters['date_fixation__gte'],holiday_date__lte=filters['date_fixation__lte']))
                
                for x in holidays:
                    if x.holiday_date.isoweekday()>=6:
                        hh['holexception'].append(x.holiday_date.strftime("%Y-%m-%d"))
                    else:
                        hh['workexception'].append(x.holiday_date.strftime("%Y-%m-%d"))
                # print(hh)
                if filters['holiday']==False:
                    self.filtershol=Q(
                                    Q(
                                Q(date_fixation__iso_week_day__lte=5), ~Q(date_fixation__in=hh['workexception']))|
                                      Q(date_fixation__iso_week_day__gte=6,date_fixation__in=hh['holexception']))
                # , ~Q(time_fixation__date__in=holidays)
                else:
                    self.filtershol=Q(Q(Q(date_fixation__iso_week_day__gte=6),~Q(date_fixation__in=hh['holexception']))|
                                      Q(date_fixation__iso_week_day__lte=6,date_fixation__in=hh['workexception'])
                                      )
            del filters['holiday']
        if 'from_ekc' in filters.keys():
            if filters['from_ekc'] is not None:
                self.filters2.append(Q(from_ekc=filters['from_ekc']))
            
            del filters['from_ekc']
        
        return filters
    
    def disable_duration(self):
        for x in ['call_duration','call_duration__gt']:
            if x in self.filters.keys():
                del self.filters[x]

    

    def getSerializer(self):
        print(self.funct)
        serializerdict={
                        'topandavg': {'district':TopandavgDistrictSerializer,'regions':TopandavgRegionsSerializer,'tnos': TopandavgTnosSerializer},
                        'previoustopavg':{'district':TopandavgDistrictSerializer,'regions':TopandavgRegionsSerializer,'tnos': TopandavgTnosSerializer},
                        'maprussia':{'district':MapDistrictSerializer, 'regions':MapRegionsSerializer},
                        'dynamic':DynamicSerializer,
                        'incomemissed':IncomemissedSerializer,
                        'functionality':FunctionalitySerializer,
                        'recall':RecallSerializer,
                        'timeclocker':TimeclockerSerializer
                        }
        if self.funct in  ['topandavg','maprussia','previoustopavg']:
            self.serializer = serializerdict[self.funct][self.to_serializer]
        else:
            self.serializer=serializerdict[self.funct]