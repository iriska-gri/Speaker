import pandas as pd
from fns.models import *
import datetime
from atc.models import *
import os
from django.conf import settings
import datetime as dt
from dateutil.parser import parse
from django.db.models import Avg, Min, Max, Sum, Count,Q,F
import numpy as np
def adupdater(filesadd):
    df = pd.read_csv(filesadd, sep=",",dtype='str')
    df['pwdLastSet'] = pd.to_datetime(df['pwdLastSet'],yearfirst=True, errors='coerce')        
    df = df[df.pwdLastSet.notnull()]                  # remove all NaT values
    
    df = df.loc[~df.company.isin(['[]','Тестовая организация','-'])]

    df = df.rename(columns={'company':'tno_name'})  
    df['tno_code']=df['sAMAccountName'].str[0:4]
    # непонятно, что делать с 
    # Дарья Александровна,Войцеховская,8(99)0000,Старший государственный налоговый инспектор,0000-315-20,2024-03-20 08:14:01.254074+00:00,2024-05-03 20:46:55.996431+00:00,ИФНС России № 1 по г. Москве,Правовой отдел,False
    # вроде ЦА, но нет. Фильтр ЦАШНИКОВ
    # df=df.loc[df.tno_code!='0000']
    
    
    df =df.loc[df['pwdLastSet'] >= pd.Timestamp("2024-01-01", tz="UTC").replace(microsecond=0)]

    df_company = df[['sAMAccountName','tno_name','department','tno_code']]
    
    # df_company['ufns__code']=
    # df_company['tno_code'].str[0:2]+'00' if df_company['tno_code'].str[0:2]!='99' else  df_company['tno_code'].str[0:4]
    df_company.loc[df_company['tno_code'].str[0:2]!='99','ufns__code']=df_company['tno_code'].str[0:2]+'00'
    df_company.loc[df_company['tno_code'].str[0:2]=='99','ufns__code']=df_company['tno_code'].str[0:4]
    df_inspection=df_company.drop(['sAMAccountName'],axis=1)
    df_otdels=df_inspection
    df_departments = df_inspection.drop_duplicates(subset=['tno_code', 'department'])
    df_inspection=df_departments.drop_duplicates('tno_code')
    
    
        

    
    ufns = pd.DataFrame.from_records(Ufns.objects.values('id','ufns_code'))
    
    ufns = ufns.rename(columns={'id':'ufns_id'})  
    df_inspection= pd.merge(df_inspection, ufns, left_on='ufns__code', right_on='ufns_code' )
    
    df_inspection=df_inspection.drop(['department','ufns_code','ufns__code'],axis=1)
    df_inspection[['ufns_id']]=df_inspection[['ufns_id']].fillna(10)
    
    
    
    for x in df_inspection.to_dict(orient='records'): 
        try: 
            if x['tno_code']=='0000':
                x['tno_name']= 'Центральный аппарат'              
            Tno.objects.update_or_create(tno_code= x['tno_code'],defaults=x)
        except Exception as e:
            print(f'ERRORRRR {x}----- {e}')
    
    tnos = pd.DataFrame.from_records(Tno.objects.values('id','tno_code'))
    tnos = tnos.rename(columns={'id':'tno_id'})  
    df_otdels = pd.merge(df_otdels, tnos, left_on='tno_code', right_on='tno_code')
    df_otdels = df_otdels.rename(columns={'department':'deps_name'})  
    df_otdels = df_otdels.drop(['tno_code', 'tno_name','ufns__code'],axis=1)
    df_otdels=df_otdels.loc[~df_otdels.tno_id.isna()]
    # print(df_otdels.loc[~df_otdels.tno_id.isna()])
    for x in df_otdels.to_dict(orient='records'): 
        try:
            Deps.objects.get_or_create(tno_id=x['tno_id'],deps_name=x['deps_name'], defaults=x)
        except Exception as e:
            print(f'ERRORRRR {x}----- {e}')
    # потом, возможно, переработать так, чтобы обновлять именно то, чего нет, если получится
    df_otdels_base =  pd.DataFrame.from_records(Deps.objects.values('id','deps_name','tno__tno_code','tno'))
    # print(Deps.objects.values('id','deps_name','tno__tno_code','tno'))
    df = df.rename(columns={'givenName':'given_name','telephoneNumber':'telephone_number',
                            'sAMAccountName': 'account_name', 'lastLogonTimestamp':'last_logon',
                            'pwdLastSet':'pwd_lastset'
                            }) 
    df = pd.merge(left=df, right=df_otdels_base, left_on=['tno_code','department'], right_on=['tno__tno_code','deps_name'], how='left')
    df = df.rename(columns={'id':'department_id'})
    df['title']=df['title'].str.lower()

    repl = [
            [' гни',' государственный налоговый инспектор'],
            ['старшийгосударственныйналоговыйинспектор','старший государственный налоговый инспектор'],
            [' госналогинспектор',' государственный налоговый инспектор'],
            ['спец.эксперт', 'специалист-эксперт'],
            ['специалист- эксперт', 'специалист-эксперт'],
            ['специалист - эксперт', 'специалист-эксперт'],
            ['заместительначальникаотдела', 'заместитель начальника отдела'],
            ['заместитель начальника отд', 'заместитель начальника отдела'],
            ['специалис-эксперт', 'специалист-эксперт'],
            ['главныйй', 'главный'],
            ['главныйгосударственный ','главный государственный '],
            ['главныйгосударственныйналоговыйинспектор','главный государственный налоговый инспектор']



    ]
    for x in ['(',')','-']:
        df['telephone_number'] = df['telephone_number'].str.replace(x,'')

    for x in repl:

        df['title']=df['title'].str.replace(x[0],x[1])
        
                            
    
    df['title']=df['title'].str.capitalize()
    pos = df[['title']].rename(columns={'title':'name'})
    pos = pos.drop_duplicates()
    
    for x in pos.to_dict(orient='records'):
        Position.objects.update_or_create(name=x['name'], defaults=x)
    pos = pd.DataFrame.from_records(Position.objects.values())
    df = pd.merge(left=df, right=pos, left_on='title',right_on='name')
    df = df.rename(columns={'id':'position_id'})
    df = df.drop(['deps_name', 'tno__tno_code','tno','department','tno_code','tno_name','distinguishedName','name','title' ],axis=1)
    
    
    for x in df.to_dict(orient='records'): 
        try:
            Ad.objects.update_or_create(account_name=x['account_name'],defaults=x)
        except Exception as e:
            pass



class AdLoader():
    def __init__(self, filestoopen) -> None:
        self.filestoopen = filestoopen
        self.loadfolder = os.path.join(settings.MEDIA_ROOT,'uploads','loadcalls')
        self.adExists = Ad.objects.values('id','sn', 'given_name', 'department__tno__ufns_id','department__tno_id','department__tno__ufns__ufns_time_difference')
        self.callscolumns = ['call_type__name',
                           
         'time_fixation','code_domen_a','number_a',
                                                'outcaller_fullname',
                                                'reg_a',
                                                'code_domen_b','number_b',
                                                'subscriber_b__fullname',
                                                'reg_b',
                                                'direction',
                                                'call_duration',
                                                
                                                'causes_disconnect__name',
                                                'source__name',
                                               
                                     ]
        self.basedrop = [
            # 'outcaller__fullname',
                         'call_type__name','ctn',
                         
                         'sn','given_name',
                         'causes_disconnect__name',
                         'department__tno__ufns_id',
                         
                         'source__name',
                         'ufns_code',
                         'department__tno_id',
                         'fullname']
 
    def loadcalls(self):
        # dates = datetime.datetime.now()
        call_type_df = pd.DataFrame.from_records(CallType.objects.values())
        call_type_df = call_type_df.rename(columns={'id':'call_type_id','name':'ctn'})
        ad = pd.DataFrame.from_records(self.adExists)
        ad['fullname'] = ad['sn'] +' '+ ad['given_name']
        
        codedomens = pd.DataFrame.from_records(Ufns.objects.values(ufid = F('id'),code=F('ufns_code')))
        

        for x in self.filestoopen:
            for df in pd.read_csv(os.path.join(self.loadfolder,x),quotechar='"',quoting=1, sep=";",dtype='str',on_bad_lines='warn', names=self.callscolumns,chunksize=100000):
                df = df.drop(['reg_a', 'reg_b', 'direction'],axis=1)
                df = df.loc[df['call_type__name'] != 'Исходящий']
                
                df['time_fixation'] =df['time_fixation'].apply(lambda x: datetime.datetime.strptime(x,'%d.%m.%Y %H:%M:%S'))
                # df['time_fixation'] = df['time_fixation'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
                df['time_fixation'] = pd.to_datetime(df['time_fixation'],yearfirst=True,).dt.tz_localize("UTC")    
                # df['call_duration']= pd.to_timedelta(df['call_duration'],unit='ms')
                df['call_duration']= pd.to_timedelta(df['call_duration'],errors='coerce')
                df['call_duration']=df['call_duration'].fillna('00:00:00')
                df['call_duration']=df['call_duration'].dt.total_seconds()
                df['ufns_code']=df['code_domen_b'].str[0:4]               
                # print(df)
                df= pd.merge(left=df, right=codedomens, left_on='ufns_code',right_on='code', how='left')                
                df['code_domen_b']=df['ufid']
                df=df.drop(['ufid' ,'code'],axis=1)
                
                
                df['ufns_a']=df['code_domen_a'].str[0:4] 
                df= pd.merge(left=df, right=codedomens, left_on='ufns_a',right_on='code', how='left') 
                df['code_domen_a']=df['ufid']
                df=df.drop(['ufid' ,'code','ufns_a'],axis=1)
                
                df = df.replace({np.nan: None})
                # df['code_domen_a']=df['code_domen_a'].fillna(0)
                # df['code_domen_a']=df['code_domen_a'].astype(int)
                # df['code_domen_b']=df['code_domen_b'].fillna(0)
                df = df.loc[~df.code_domen_b.isna()]
                df['code_domen_b']=df['code_domen_b'].astype(int)
                df = pd.merge(left=df, right=ad, left_on=['code_domen_b','subscriber_b__fullname'],right_on=['department__tno__ufns_id','fullname'], how='left')
                            
                df = pd.merge(df, call_type_df, left_on='call_type__name', right_on='ctn')               
                 
                
                df = df.rename(columns={'id':'subscriber_b_id','code_domen_a':'code_domen_a_id','code_domen_b':'code_domen_b_id'})
                noad = df.loc[df.subscriber_b_id.isna()]
                # print(df)
                # noad = df.loc[df.subscriber_b_id==0]
                
                noad=noad.drop(['department__tno__ufns__ufns_time_difference'],axis=1)
                df = df.loc[df.subscriber_b_id>0]
                df["time_fixation"] = [datetime.timedelta(hours=tz)+dt
                            for dt,tz in zip(df["time_fixation"], df['department__tno__ufns__ufns_time_difference'])]

                print(df)
                
                df = df.drop(self.basedrop+['subscriber_b__fullname','department__tno__ufns__ufns_time_difference'],axis=1)
                
                
                df = [Calls(**x) for x in df.to_dict(orient='records')]
                
                Calls.objects.bulk_create(df, ignore_conflicts=True)
                
                
                noad['ufns_code']=noad['code_domen_b_id'] 
                      
                newuser= noad[['ufns_code', 'subscriber_b__fullname','number_b']]
                 
                newuser['account_name']= newuser['ufns_code'].astype(str).str.zfill(4)+'-tel-'+newuser['number_b']+newuser['subscriber_b__fullname']
                print(newuser)  
                print("------------------------") 
                tnos = pd.DataFrame.from_records(Tno.objects.values('id','tno_code','ufns_id'))
                
                newuser = pd.merge(left=newuser, right=tnos, left_on='ufns_code',right_on='ufns_id')
                
                newuser =newuser.rename(columns={'id':'tno_id','subscriber_b__fullname':'sn'})
                # print(newuser)
                newuser = newuser.drop('ufns_id',axis=1)
                newdeps = newuser[['tno_id']]
                newdeps=newdeps.drop_duplicates()
                newdeps['deps_name']='Нет в AD'
                
                newdeps = [Deps(**x) for x in newdeps.to_dict(orient='records')]
                
                Deps.objects.bulk_create(newdeps, ignore_conflicts=True) 

                nd = pd.DataFrame.from_records(Deps.objects.filter(deps_name='Нет в AD').values('id','deps_name','tno__tno_code', 'tno'))
                # print(nd)
                newuser = pd.merge(left=newuser, right=nd, left_on='tno_id',right_on='tno')
                newuser =newuser.rename(columns={'id':'department_id'})                
                newuser = newuser.drop_duplicates(subset=['sn','number_b','account_name'])
                newuser['telephone_number']= '8'+ newuser["tno_code"].str[0:2] + newuser["number_b"]
                newuser = newuser.drop(['ufns_code', 'number_b','tno','tno_id','tno_code','deps_name','tno__tno_code'] ,axis=1)
                newuser  = [Ad(**x) for x in newuser.to_dict(orient='records')]
                Ad.objects.bulk_create(newuser, ignore_conflicts=True)
                no_ad=pd.DataFrame.from_records(Ad.objects.filter(department__deps_name='Нет в AD').values('id','sn','department__tno__ufns__ufns_time_difference'))
                noadcalls = noad.drop(self.basedrop+  ['subscriber_b_id'],axis=1)
                noadcalls = noadcalls.rename(columns={'id':'department_id'})
                noadcalls = pd.merge(left = noadcalls, right=no_ad, left_on='subscriber_b__fullname',right_on='sn' )
                
                noadcalls["time_fixation"] =  [datetime.timedelta(hours=tz)+dt
                            for dt,tz in zip(noadcalls["time_fixation"], noadcalls['department__tno__ufns__ufns_time_difference'])]
            
                noadcalls =noadcalls.rename(columns={'id':'subscriber_b_id'})
                noadcalls = noadcalls.drop(['sn','subscriber_b__fullname','department__tno__ufns__ufns_time_difference'],axis=1)
                noadcalls = [Calls(**x) for x in noadcalls.to_dict(orient='records')]
                Calls.objects.bulk_create(noadcalls, ignore_conflicts=True)
        