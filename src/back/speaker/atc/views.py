from django.shortcuts import render
from rest_framework.views import APIView
from django.db.models import Count
# Create your views here.
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import *
import pandas as pd
from fns.models import *
from django.db.models import Avg, Min, Max, Sum, Count,Q,F,ExpressionWrapper, Value, Func
import datetime
from django.db.models.functions import TruncDate, ExtractHour, Cast,Concat
from django.db.models.functions.comparison import NullIf
from .serializers import *
from .GetLevelInfoH import QD, QDBAD
from .CallinfoH import CallinfoHqueryBuildier,CallinfoCalculator
from adrf.views import APIView as AAPIView
import asyncio
from asgiref.sync import sync_to_async
from django.db.models.functions import Length
import dateutil.parser
from itertools import chain
from functools import reduce
import operator
class GetCalldates(APIView):
    '''
    Получить 2 даты из бд
    '''
    def get(self, request):
        a=CallsView.objects.order_by('date_fixation').last()
        b=CallsView.objects.filter(date_fixation__lte=(a.date_fixation-datetime.timedelta(days=7))).order_by('-date_fixation').first()
        print(a, b)
        return Response([a.date_fixation,b.date_fixation])




class GetCallInfo(AAPIView,CallinfoHqueryBuildier, CallinfoCalculator):
    @swagger_auto_schema( request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'funct': openapi.Schema(type=openapi.TYPE_STRING, description='то, что в данный момент надо посчитать'),
        'filters': openapi.Schema(type=openapi.TYPE_OBJECT, description='Подготовленные фильтры из store'),
    }
))
    async def post(self, request)->dict:
        """
        получить отфильтрованные данные звонков
        # maprussia: для карты
        funct: topandavg (таблица, ТОП-5 по принятым звонкам, ТОП-5 по пропущенным звонкам)
        dynamic (Динамика длительности звонков,
         incomemissed: Динамика количества принятых и пропущенных звонков),
         functionality (Звонки по функциональным направлениям)
         recall (динамика повторных)
         timeclocker (нагрузка по часам)
      """
        data = request.data
        self.filters2=[]
        self.filtershol=Q()
        self.funct =  data['funct']   
        self.filters = await  self.getvalandfilters(data['filters'])          
        self.getSerializer() 
        # if self.funct in ['topandavg','previoustopavg','functionality','incomemissed','dynamic','recall']:
        now = datetime.datetime.now()
    
        r=await asyncio.create_task(getattr(self,self.funct)())
        print(self.funct, datetime.datetime.now()-now)
        a = self.serializer(r, many=True).data
        # else:
        #     a=[]
        return Response(a)
        
    
    async def topandavg(self):
        now = datetime.datetime.now()
        self.disable_duration()       
        
        # Базовый запрос
        print(self.filters,self.filters2)
        base= CallsView.objects.filter(self.filtershol,*self.filters2, **self.filters,)                                    
        baseval = base.values(*self.val)
        a=baseval
        c= base
        diff=(datetime.datetime.strptime(self.filters['date_fixation__lte'],"%Y-%m-%d").date()-datetime.datetime.strptime(self.filters['date_fixation__gte'],"%Y-%m-%d").date()).days +1
        print(diff)
        a= self.qgetter(a.annotate(
                    avg=Sum('callsumb')/NullIf(Sum('acceptedb'),0),
                    total=Sum('totalb'), 
                    missed = Sum('missedb'),
                    dropped= Sum('droppedb'),
                    callsum = Sum('callsumb'),
                    personsday=Sum('personsdayb'),
                    
                    ))        
        b = self.qgetter(CallsViewPerson.objects.filter(self.filtershol,*self.filters2, **self.filters).values(self.idval).annotate(persons = Count('subscriber_b', distinct=True)))
        
        [a,b]=await asyncio.gather(*[a,b])
        print(b)
        a = self.persons_personsday_counter(a,b)
        return a
    
 
    async def qgetter(self,q):        
        return await sync_to_async(list, thread_sensitive=False)(q)
        
        
    
    async def previoustopavg(self):       
        return await self.topandavg()
    
    

    async def dynamic(self):
        self.disable_duration() 
        a = await sync_to_async(list,thread_sensitive=False)(CallsView.objects.filter(**self.filters).filter(*self.filters2)\
                                      .filter(self.filtershol)\
                                     .values('date_fixation')\
            .annotate(call_timedelta_avg=Sum('callsumb')/NullIf(Sum('acceptedb'),0)
            ).order_by('date_fixation'))
        
        return a
   
    
    
    async def incomemissed(self):
        self.disable_duration()    

        a = await sync_to_async(list,thread_sensitive=False)(CallsView.objects.filter(**self.filters).filter(*self.filters2)\
                                      .filter(self.filtershol)\
                                      .annotate(day=F('date_fixation')).values('day')\
                    .annotate(
                       missed = Sum('missedb'),
                    dropped= Sum('droppedb'),
                    accepted= Sum('acceptedb'),
                    total=Sum('totalb')
                     
            ).order_by('day'))

      
        return a
    
    async def functionality(self):
        self.disable_duration()
        a=await sync_to_async(list,thread_sensitive=False)(CallsView.objects.filter(self.filtershol,*self.filters2, **self.filters)\
                                    .values('depdirection','depdirection__name').annotate(
                missed = Sum('missedb'),
                    dropped= Sum('droppedb'),
                    total=Sum('totalb')))
        
                      
            
    
        return a


    async def recall(self):        
        print("RECALL ST")   
        now = datetime.datetime.now()    
        self.disable_duration()    
     
        # Жестко длина >= 10
        a = await sync_to_async(list,thread_sensitive=False)(CallsView.objects.filter(self.filtershol,**self.filters).filter(*self.filters2).annotate(day=F('date_fixation')).values('day')\
        .annotate(recall=Sum('recallb'),
                   total=Sum('totalmorenineb')
                  ))
      
       
        return a
   

    async def timeclocker(self):
        
        self.disable_duration()
        a = await sync_to_async(list,thread_sensitive=False)(CallsViewClocker.objects.filter(**self.filters).filter(*self.filters2)\
                                      .filter(self.filtershol)\
                                      .values('hour')\
            .annotate( 
                    accepted = Sum('accepted'),
                    missed = Sum('missed'),
                    dropped= Sum('dropped'),
                    total=Sum('total')
                     
            ).order_by('hour'))       
        

        return a




class GetLevelInfo(AAPIView):
    @swagger_auto_schema( request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'level': openapi.Schema(type=openapi.TYPE_STRING, 
        description='вывод данных полученных по значнию ключа level', example='federal'),
        'indicator':openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING),
                                   description='список функций для расчета', example=['countcalls','accepted','missed','worktime','nowork','avgtime','callpeak']),
        'filters':openapi.Schema(type=openapi.TYPE_OBJECT,
                                   description='фильтры'),                           
    }
    )
)
    async def addfilter(self, filters):
        if 'holiday' in filters.keys():
          
            hh={'workexception':[],
                'holexception':[],
                }
            if filters['holiday'] is not None:
                    holidays =await  sync_to_async(list,thread_sensitive=False)(HolidayExculisions.objects.filter(holiday_date__gte=filters['date_fixation__gte'],holiday_date__lte=filters['date_fixation__lte']))
                    
                    for x in holidays:
                        if x.holiday_date.isoweekday()>=6:
                            hh['holexception'].append(x.holiday_date.strftime("%Y-%m-%d"))
                        else:
                            hh['workexception'].append(x.holiday_date.strftime("%Y-%m-%d"))
                    
                    if filters['holiday']==False:
                        self.filtershol=Q(
                                        Q(
                                    Q(date_fixation__iso_week_day__lte=5), ~Q(date_fixation__in=hh['workexception']))|
                                        Q(date_fixation__iso_week_day__gte=6,date_fixation__in=hh['holexception']))
                    
                    else:
                        self.filtershol=Q(Q(Q(date_fixation__iso_week_day__gte=6),~Q(date_fixation__in=hh['holexception']))|
                                        Q(date_fixation__iso_week_day__lte=6,date_fixation__in=hh['workexception'])
                                        )
        del filters['holiday']

        return filters
    
    
    async def post(self,request):
        print('GetLevelInfo')
        self.now = datetime.datetime.now()
        data = request.data        
        self.level =  data['level']  
        print(data['filters'])
        self.filtershol=Q()  
        self.filters=await self.addfilter(data['filters'])
        self.diff=(datetime.datetime.strptime(self.filters['date_fixation__lte'],"%Y-%m-%d").date()-datetime.datetime.strptime(self.filters['date_fixation__gte'],"%Y-%m-%d").date()).days +1
        self.newcolumns = []
        self.qHELP = QD(self.level, self.diff)    
       
        print(self.level)
        self.gatherer=[]
        aggekc=Q()
        if 'from_ekc' in self.filters and self.filters['from_ekc'] is not None:
            aggekc=Q(from_ekc=self.filters['from_ekc'])
        else:
            del self.filters['from_ekc']
        avginatorq =CallsViewPerson.objects.filter(date_fixation__gte=self.filters['date_fixation__gte'],
                                         date_fixation__lte=self.filters['date_fixation__lte']
                                          ).filter(self.filtershol).filter(aggekc)
       
        subday=self.foo(None)
        peak=self.foo({})
        cp=self.foo(None)
       
        personing=self.foo(None) 

      
        avginator=avginatorq.aaggregate(**self.qHELP.avgaggregator(data['indicator']))

        self.gatherer =[avginator, peak,subday]
  
               
        BASETABLE = CallsViewPerson
        

        print(datetime.datetime.now()-self.now)   

        base = BASETABLE.objects.filter(**self.filters).filter(self.filtershol)
    
        b=base.values(*self.qHELP.qarr['base']).annotate(**self.qHELP.qarr['annotate'],**self.qHELP.qarr['rename'])
        
            
        for x in data['indicator']:
         
            if x not in ['callpeak']:
                b = getattr(self, x)(b)
                self.newcolumns.append(x)
        # if self.level=='sub_b':
        #     b = b.annotate(person=Func(F('subscriber_b__given_name'),Value(' '),F('subscriber_b__sn'), function= 'CONCAT'))
        
        b =sync_to_async(list,thread_sensitive=False)(b.values(*self.qHELP.qarr['vl'], *self.newcolumns))
        self.gatherer.append(b)
        if 'callpeak' in data['indicator']:
            cp=self.callpeak()
        self.gatherer.append(cp)
        

        if 'personloading' in data['indicator']:
            personing =  sync_to_async(list,thread_sensitive=False)(base.values('date_fixation',self.qHELP.qarr['counter']).order_by('date_fixation')\
                                            .annotate(personsday=NullIf(Count('subscriber_b', distinct=True),0)))
        self.gatherer.append(personing)
        
        
        
        

        # print(self.gatherer)
        avginator,peak,subday,b,cp,personing = await asyncio.gather(*self.gatherer)
        
        # # print(personing)
        
        
      
        if 'callpeak' in data['indicator'] and cp.size>0:    
            # print(cp)

            n = pd.DataFrame(b)            
            b = pd.merge(n,cp, on=self.qHELP.indigroup())
            b=b.fillna(0)
           
            b = b.to_dict(orient='records')

        
      
        print(datetime.datetime.now()-self.now) 
        return Response({'avgrussia': avginator, 'data': b})            
    




    
    
    
    def countcalls(self, b): 
        return b.annotate(countcalls=Sum('totalb'))
    
    def avgtime(self, b):  
        
        b= b.annotate(avgtime=ExpressionWrapper((Sum('callsumb')+0.0)/NullIf((Sum('acceptedb')+0.0),0), models.FloatField()))
        return b    
             

    def accepted(self,b):
        b = b.annotate(accepted= Sum('acceptedb')                       
                       )       
        return b

    def accepted_p(self,b):
        b=b.annotate(accepted_p= ExpressionWrapper((Sum('acceptedb')+0.0)*100/NullIf((Sum('totalb')+0.0),0), models.FloatField()))
        return b
    
    def missed(self,b):  
        b = b.annotate(missed= Sum('missedb'),
                    #    missed_p= ExpressionWrapper((Count('id',filter=Q(call_duration=0))+0.0)*100/(Count('id')+0.0), models.FloatField()),
                       )     
        # self.newcolumns.append('missed_p')  
        return b
    def missed_p(self,b):  
        b = b.annotate(missed_p= ExpressionWrapper((Sum('missedb')+0.0)*100/NullIf((Sum('totalb')+0.0),0), models.FloatField()),
                       )     
        
        return b

    
    def dropped(self,b):  
        b = b.annotate(dropped= Sum('droppedb'),
                    #    dropped_p= ExpressionWrapper((Count('id',filter=Q(call_duration__gt=0, call_duration__lte=3))+0.0)*100/(Count('id')+0.0), models.FloatField()),
                       )     
        
      
        
        return b
    def dropped_p(self,b):  
        b = b.annotate(dropped_p= ExpressionWrapper((Sum('droppedb')+0.0)*100/NullIf((Sum('totalb')+0.0),0), models.FloatField()),
                       )     

      
        
        return b

    async def callpeak(self):
        print("CP")

        cp=[]
      
        if self.level!='sub_b' and ('subscriber_b__sn__icontains' not in self.filters):
            cp = await sync_to_async(list,thread_sensitive=False)(CallsViewClocker.objects.filter(**self.filters).filter(self.filtershol)\
                .values('hour', *self.qHELP.qarr['base']).annotate(**self.qHELP.qarr['rename'])\
            .annotate(callpeak=F('hour'),maxhc=Count(F('callpeak'))).values(self.qHELP.indigroup(),'maxhc', 'callpeak')
            )
        else:
            exc=Q()
            inc = Q()
            self.qHELPBAD = QDBAD(self.level)
            if 'from_ekc' in self.filters and self.filters['from_ekc'] is not None:
                if self.filters['from_ekc']==True:
                    inc = reduce(operator.or_, (Q(outcaller_fullname__icontains=x) for x in ['екц','единый']))
                    exc=reduce(operator.and_, (~Q(outcaller_fullname__icontains=x) for x in ['инспекции']))
                else:
                    exc = reduce(operator.or_, (~Q(outcaller_fullname__icontains=x) for x in ['екц','единый']))
                    print(exc)
            cp = await sync_to_async(list,thread_sensitive=False)(Calls.objects.filter(**self.qHELPBAD.filtersmaker(self.filters))\
                .filter(inc).filter(exc)\
                .annotate(date_fixation=F('time_fixation')).filter(self.filtershol)\
                .values(*self.qHELPBAD.qarr['base']).annotate(**self.qHELPBAD.qarr['rename'])\
            .annotate(callpeak=F('time_fixation__hour'),maxhc=Count(F('callpeak')))
                    #   .values(self.qHELP.indigroup(),'maxhc', 'callpeak'))
            )
        df = pd.DataFrame(cp)
        # print(df)
        if df.size>0:        
        
            df = (df.groupby([self.qHELP.indigroup()], as_index=False)
                .apply(lambda x: x.nlargest(1,['maxhc']))
                .reset_index(level=0, drop=True))
            if self.level=='sub_b' and ('subscriber_b__sn__icontains' not in self.filters):
                df = df.drop(['maxhc',*self.qHELPBAD.qarr['base']],axis=1)
            else:
                df = df.drop('maxhc',axis=1)
      

        return df    

        


    
    def worktime(self, b):
        b= b.annotate(worktime=Sum('totalb', filter=Q(wt=True)))
    
        return b
    
    def nowork(self, b):
        b= b.annotate(nowork=Sum('totalb', filter=Q(wt=False))   )    
        
        return b
    

    def countcalls_to_person(self,b):
        b = self.countcalls(b)        
        # b = b.annotate(personcount=)

        b = b.annotate(countcalls_to_person=Sum('totalb')/NullIf(Count('subscriber_b', distinct=True),0))

        return b

    def personloading(self,b):
        # Загруженность сотрудников
        b = b.annotate(callsum=Sum('callsumb'),
                       personloading=ExpressionWrapper((F('callsum')+0.0)/(NullIf(Count('subscriber_b')*60*60*8,0))*100,models.FloatField() )
                       
                       )

        # b = b.annotate(subday = Count(Concat('date_fixation','subscriber_b'),distinct=True), personloading=ExpressionWrapper((F('callsum')+0.0)/(F('subday')*60*60*8)*100,models.FloatField() ))
        # 
        self.newcolumns.append('callsum')  
        return b
    
    async def foo(self, returnit):
        await asyncio.sleep(.0001)
        return returnit
   



class TestInfo(AAPIView):
    def get(self,request):
        print("Sssssaaaaaak")
        a = CallsView.objects.all()
        # print(list(a))
        return Response("ssss")
    