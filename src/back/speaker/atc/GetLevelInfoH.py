from .serializers import *
from django.db.models import Avg, Min, Max, Sum, Count,Q,F,ExpressionWrapper, DateTimeField, IntegerField
from django.db.models.functions import Concat
from django.db.models import F, Value, CharField
from django.db.models.functions.comparison import NullIf
class QD():
    def __init__(self ,level,diff) -> None:
        self.level=level
        self.diff=diff
        self.grouparr = self.getgroup() # Группировка датафрейма
        self.qarr = getattr(self,level)() # Массив для values queryset
        # self.serializer=getattr(self,'getserializer')() # Сериализатор
        
        self.avginatoraggdict={
                'avg_duration':ExpressionWrapper((Sum('callsumb')+0.0)/Sum('acceptedb'), models.FloatField()),
                'total': Sum('totalb'), 
                'totalels': Count(self.qarr['counter'], distinct=True),
                'missed': Sum('missedb'),                      
                'dropped': Sum('droppedb'),
                'worktime': (Sum('totalb', filter=Q(wt=True))),
                'countcalls_to_person': ExpressionWrapper(Sum('totalb')/NullIf(Count('subscriber_b', distinct=True),0), models.FloatField()),                           
                # 'distperson': Sum('personsdayb')/self.diff,
                'personloading': ExpressionWrapper(Sum('callsumb')*100/(NullIf(Count('subscriber_b')*60*60*8,0)),models.FloatField())
        }
        
        
        
        
        pass
    
    def federal(self):
       
        return {
            'counter':'district_id',
            'newcounter':'district_id',
            
            'base':[
                    
                        "district_id",
                     "district__district_name",
                
                        
                        ],
                'vl':[                   
                    'district_id',
                      'district',
                      'region',
                      'tno','department','person'                      
                      ],
             
                'rename':{
                        # 'district_id':F('district_id'),
                        'district': F('district__district_name')
                },

                
                'annotate':{
                    'region':Count('ufns_id',distinct=True),
                    'tno':Count('tno_id',distinct=True),
                    'department':Count('department_id',distinct=True),
                    'person': Count('subscriber_b', distinct=True)
                },
                
                
                }
        
    def ufns(self):      

        return {
            'counter':'ufns_id',
            'newcounter':'ufns_id',
          
            'base':[            
            "district__id",
            "district__district_name",
            "ufns__ufns_name",
            "ufns_id",
           
                ],
                'vl':[
                    # 'id','call_duration','time_fixation',
                    'district_id',
                      'district','region','ufns_id','tno','department','person'                      
                      ],
                'annotate':{                    
                    'tno':Count('tno_id',distinct=True),
                    'department':Count('department_id',distinct=True),
                    'person': Count('subscriber_b', distinct=True)
                },
                'rename':{
                        # 'district_id':F('subscriber_b__department__tno__ufns__district__id'),
                        'district': F('district__district_name'),
                        'region':F("ufns__ufns_name"),
                        # 'ufns_id':F("ufns_id"),
                },
                }
    
    def tno(self):
    
        return {
            'counter':'tno_id',
            'newcounter':'tno_id',
            'base':[
            # 'id','call_duration','time_fixation',
            "district__id",
            "district__district_name",
            "ufns__ufns_name",
            "ufns_id",
                      "tno_id",
                      "tno__tno_name",
                    #    "subscriber_b__department__id",
                    #    "subscriber_b__id"
                        
                        ],
                'vl':[
                    # 'id','call_duration','time_fixation',
                    'district_id',
                      'district','region','ufns_id','tno_id','tno','department','person'                      
                      ],
                 'annotate':{                    
                    
                    'department':Count('department_id',distinct=True),
                    'person': Count('subscriber_b', distinct=True)
                },
                'rename':{
                        # 'district_id':F('subscriber_b__department__tno__ufns__district__id'),
                        'district': F('district__district_name'),
                        'region':F("ufns__ufns_name"),
                        # 'ufns_id':F("subscriber_b__department__tno__ufns__id"),
                        # 'tno_id':F('subscriber_b__department__tno__id'),
                        'tno':F('tno__tno_name')

                },
                }
        
    def dep(self):
        
        return {
            'counter':'department_id',
            'newcounter':'department_id',
            'base': [ 
                "district__id",
            "district__district_name",
            "ufns__ufns_name",
            "ufns_id",
                      "tno_id",
                      "tno__tno_name",
                       "department_id",
                       "department__deps_name",                     
                        
                        ],
                'vl':[
                    # 'id','call_duration','time_fixation',
                    'district_id',
                      'district','region','ufns_id','tno_id','tno','deps_id','department','person'                      
                      ],
                      'annotate':{                                
                    
                    'person':  Count('subscriber_b', distinct=True)
                },
                      'rename':{
                        # 'district_id':F('subscriber_b__department__tno__ufns__district__id'),
                        'district': F('district__district_name'),
                        'region':F("ufns__ufns_name"),
                        # 'ufns_id':F("subscriber_b__department__tno__ufns__id"),
                        # 'tno_id':F('subscriber_b__department__tno__id'),
                        'tno':F('tno__tno_name'),
                        'deps_id':F("department_id"),
                        'department':F("department__deps_name")

                },
                }




    def sub_b(self):
     
        # return sub_b
        return {
            'counter':'subscriber_b__id',
            'newcounter':'sub_b_id',
            'base':[
            # 'id','call_duration','time_fixation',
               "district__id",
            "district__district_name",
            "ufns__ufns_name",
            "ufns_id",
                      "tno_id",
                      "tno__tno_name",
                       "department_id",
                       "department__deps_name",    
                       "subscriber_b",'subscriber_b__disabled','subscriber_b__pwd_lastset',
                        'person'
                        ],
                'vl':[
                    # 'id','call_duration','time_fixation',
                    'district_id',
                      'district','region','ufns_id','tno_id','tno','deps_id','department',
                      'sub_b_id','disabled','pwd_lastset','person' 
                                           
                      ],
                 'rename':{
                        # 'district_id':F('subscriber_b__department__tno__ufns__district__id'),
                        'district': F('district__district_name'),
                        'region':F("ufns__ufns_name"),
                        # 'ufns_id':F("subscriber_b__department__tno__ufns__id"),
                        # 'tno_id':F('subscriber_b__department__tno__id'),
                        'tno':F('tno__tno_name'),
                        'deps_id':F("department"),
                        'department':F("department__deps_name"),
                        'sub_b_id':F("subscriber_b"), 
                        
                        'disabled': F('subscriber_b__disabled'),
                        'pwd_lastset':F('subscriber_b__pwd_lastset')


                },
                 'annotate':{                                                 
                    
                },
                }
     

    def getgroup(self):
        groupdict = {
            'federal':['district_id','district'],
            'ufns': ['district_id','district','ufns_id','region'],
            'tno':['district_id','district','ufns_id','region','tno_id','tno'],
            'dep':['district_id','district','ufns_id','region','tno_id','tno','deps_id','department'],
            'sub_b':['district_id','district','ufns_id','region','tno_id','tno', 'deps_id','department','sub_b_id', 'person' ]
                        # ,
        }
        print
        return groupdict[self.level]
    
    # def getserializer(self):
    #     serializers = {
    #         'federal': DistrictSerializer,
    #         'ufns': UfnsSerializer,
    #         'tno':TnoSerializer,
    #         'dep':DepSerializer,
    #         'sub_b':SubBSerializer
    #     }
    #     return serializers[self.level]
    # def basegroup(self):
    #     gr = {
    #         'federal':'subscriber_b__department__tno__ufns__district__id',
    #         'ufns': 'subscriber_b__department__tno__ufns__id',
    #         'tno': 'subscriber_b__department__tno__id',
    #         'dep':'subscriber_b__department__id',
    #         'sub_b':'subscriber_b__id'
    #      }
    #     return gr[self.level]
    def indigroup(self):
        gr = {
            'federal': 'district_id',
            'ufns': 'ufns_id',
            'tno': 'tno_id',
            'dep':'deps_id',
            'sub_b':'sub_b_id'


        }
        return gr[self.level]
    
    def avgaggregator(self,indicators):
        # Собирает необходимые поля для агрегатора средних значений в зависимости от фильтров
        avgq = {}
        for x in indicators:
            avgq['totalels']=self.avginatoraggdict['totalels']
            if x == 'countcalls':
                avgq['total']=self.avginatoraggdict['total']
            if x=='countcalls_to_person':
                avgq['total']=self.avginatoraggdict['total']
                avgq['countcalls_to_person']=self.avginatoraggdict['countcalls_to_person']
            if x in ['missed','missed_p','accepted','accepted_p','dropped','dropped_p']:
                avgq['total']=self.avginatoraggdict['total']
                avgq['missed']=self.avginatoraggdict['missed']
                avgq['dropped']=self.avginatoraggdict['dropped']
            # elif x in ['dropped','dropped_p']:
            if x=='avgtime':
                avgq['avg_duration']=self.avginatoraggdict['avg_duration']  
        
            if x in ['worktime','nowork']:
                avgq['total']=self.avginatoraggdict['total']
                avgq['worktime']=self.avginatoraggdict['worktime'] 
            
            if x=='personloading':
                avgq['personloading']=self.avginatoraggdict['personloading']
            # if x=='countcalls_to_person':
            #     avgq['total']=self.avginatoraggdict['total']
            #     avgq['countcalls_to_person']=self.avginatoraggdict['distperson']
        return avgq
    


class QDBAD():
    def __init__(self ,level) -> None:
        self.level=level
        
        self.grouparr = self.getgroup() # Группировка датафрейма
        self.qarr = getattr(self,level)() # Массив для values queryset
        # self.serializer=getattr(self,'getserializer')() # Сериализатор
        self.selectrelaterd = ['subscriber_b','subscriber_b__department','subscriber_b__department__tno','subscriber_b__department__tno__ufns','subscriber_b__department__tno__ufns__district']
               
        self.filtersdict={
            
            'district_id__in':'subscriber_b__department__tno__ufns__district__id__in',
            'ufns_id__in':"subscriber_b__department__tno__ufns__id__in",
            'tno_id__in':"subscriber_b__department__tno_id__in",
            'date_fixation__gte':'time_fixation__date__gte',
            'date_fixation__lte':'time_fixation__date__lte',
            'subscriber_b__sn__icontains':'subscriber_b__sn__icontains',
            'department_id':'subscriber_b__department_id',
            'subscriber_b':'subscriber_b__id',
            'department__deps_name__icontains': 'subscriber_b__department__deps_name__icontains'
        }
        
        pass

    def filtersmaker(self,filters):
        

        filter = {}
        for (x,v) in filters.items():
            if(x!='from_ekc'):
                filter[self.filtersdict[x]]=v
     
        return filter
    
    def federal(self):
       
        return {         
            
            'base':[
                    
                        "subscriber_b__department__tno__ufns__district__id",
                    
                
                        
                        ],
          
             
                'rename':{
                        'district_id':F('subscriber_b__department__tno__ufns__district__id'),
                     
                },

            
                
                }
        
    def ufns(self):      

        return {
           
            'base':[            
            
            "subscriber_b__department__tno__ufns__id",
           
                ],
          
                'rename':{
                     
                        'ufns_id':F("subscriber_b__department__tno__ufns__id"),
                },
                }
    
    def tno(self):
    
        return {
        
            'base':[         
           
                      "subscriber_b__department__tno__id",
                   
                        
                        ],
            
                'rename':{
                    
                       
                        'tno_id':F('subscriber_b__department__tno__id'),
                      

                },
                }
        
    def dep(self):
        
        return {
         
            'base': [ 
                       "subscriber_b__department__id",
                               
                        
                        ],
              
                      'rename':{
                       
                        'deps_id':F("subscriber_b__department__id"),
                       
                },
                }




    def sub_b(self):
     
        # return sub_b
        return {
      
            'base':[          
          
                       "subscriber_b__id"
                        ],
               
                 'rename':{
                        
                        'sub_b_id':F("subscriber_b__id"),                      
                       


                },
               
                }
     

    def getgroup(self):
        groupdict = {
            'federal':['district_id','district'],
            'ufns': ['district_id','district','ufns_id','region'],
            'tno':['district_id','district','ufns_id','region','tno_id','tno'],
            'dep':['district_id','district','ufns_id','region','tno_id','tno','deps_id','department'],
            'sub_b':['district_id','district','ufns_id','region','tno_id','tno', 'deps_id','department','sub_b_id', 'person' ]
                        # ,
        }
        print
        return groupdict[self.level]