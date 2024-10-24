import { defineStore } from "pinia";
import { api } from 'boot/axios'
import { format_date_to_base } from '../js/formatters'
import moment from "moment";
import { ref, watch, computed } from "vue";
import { date } from 'quasar'
export const useFilterStore = defineStore("filter",()=> {
    const percenterview = ref(true)
    const apicontroller = ref(new AbortController());
    const addictFilters = ref({
        tno:[],
        // department:[],
        // person:[],
        indicator:[
          {id:0, label:"Количество", shortlabel: "Количество",field:'countcalls',name:'countcalls', style: 'width: 7%', headerStyle: 'width: 5%',align: 'right',sortable:true,defaultshow:true},
        
          {id:2, label:"Рабочее время (кол-во)", shortlabel: "Рабочее время",field:'worktime',name:'worktime', style: 'width: 5%', headerStyle: 'width: 6%', align: 'right',sortable:true,defaultshow:false},
          {id:4, label:"Нерабочее время (кол-во)", shortlabel: "Нерабочее время",field:'nowork',name:'nowork', style: 'width: 5%', headerStyle: 'width: 6%', align: 'right',sortable:true,defaultshow:false},
          {id:6, label:"Звонков на сотрудника (шт)", shortlabel: "Звонков на сотрудника",field:'countcalls_to_person',name:'countcalls_to_person', style: 'width: 7%', headerStyle: 'width: 5%',align: 'right',sortable:true,defaultshow:true},
          {id:8, label:"Сброшенные % ", shortlabel: "Сброшенные", field:'dropped_p', name:'dropped_p', style: 'width: 9%', headerStyle: 'width: 7%', align: 'right',sortable:true,defaultshow:false, format:val=> !!val?parseFloat(val.toFixed(2)):0},
          {id:10, label:"Сброшенные (шт.)", shortlabel: "Сброшенные", field:'dropped', name:'dropped', style: 'width: 9%', headerStyle: 'width: 7%', align: 'right',sortable:true,defaultshow:false},
          {id:12, label:"Пропущенные %", shortlabel: "Пропущенные", field:'missed_p', name:'missed_p', style: 'width: 9%', headerStyle: 'width: 7%', align: 'right',sortable:true ,defaultshow:false, format:val=> !!val?parseFloat(val.toFixed(2)):0},
          {id:14, label:"Пропущенные (шт.)", shortlabel: "Пропущенные", field:'missed', name:'missed', style: 'width: 9%', headerStyle: 'width: 7%', align: 'right',sortable:true ,defaultshow:false},
          {id:16, label:"Принятые %", shortlabel: "Принятые%",field:'accepted_p',name:'accepted_p', style: 'width: 9%', headerStyle: 'width: 7%', align: 'right',sortable:true,defaultshow:true, format:val=> !!val?parseFloat(val.toFixed(2)):0},
          {id:18, label:"Принятые (шт.)", shortlabel: "Принятые шт",field:'accepted',name:'accepted', style: 'width: 9%', headerStyle: 'width: 7%', align: 'right',sortable:true,defaultshow:true, },
          {id:20, label:"Текущая загруженность %", shortlabel: "Загруженность",field:'personloading',name:'personloading', style: 'width: 9%', headerStyle: 'width: 7%', align: 'right',sortable:true,defaultshow:true, format:val=> !!val?parseFloat(val.toFixed(2)):0},
          {id:22, label:"Средняя длительность", shortlabel: "Ср. длительность",field:'avgtime',name:'avgtime', style: 'width: 110px', headerStyle: 'width: 80px',defaultshow:true, format:val=> !!val?moment.unix(Math.round(val)).format('m мин ss сек'):0, align: 'right',sortable:true, },
          {id:24, label:"Пик звонков (ч,мест.вр)", shortlabel: "Пик",field:'callpeak',name:'callpeak', style: 'width: 5%', headerStyle: 'width: 6%', align: 'right',sortable:true,defaultshow:false},
        ],
        
        level:[
          {id:1, name:"Федеральный округ", level:"federal"},{id:2, name:"Регион", level:"ufns"},
          {id:3, name:"Инспекция", level:"tno"},
          {id:4, name:"Отдел", level:"dep"},
           {id:5, name:"Сотрудник", level:"sub_b"}
        ]

    })

    const mainFilters= ref({
      mapscale: 
      [
        { name: "Федеральные округа", id: 1 },
        { name: "Регионы", id: 2 },
      ],
      direction:[],
      
      district: [
       
      ],
      regions: [
       
      ],

      call_type: [
        {name:"Все", id:null}
      ],

      call_duration: [
        {name:"Все", id:null,field:'total' },
        { name: "Принятые", id: 1,field:'accepted' },
        { name: "Пропущенные", id: 2, field:'missed' },
        { name: "Сброшенные", id: 3, field:'dropped' },
      ],

      call_time_msc: [
        {name:"Всё", id:null,field:0 },
        { name: "Рабочее", id: 1 ,field:'worktime'},
        { name: "Нерабочее", id: 2 ,field:'nowork'},
      ],

      holiday: [
        {name:"Все", val: null},
        {name: "Рабочие", val: false},
        {name: "Выходные", val: true},
      ],

      from_ekc: [
        {name:"Все", val: null},
        {name: "Не из ЕКЦ", val: false},
        {name: "Из ЕКЦ", val: true},

      ],

    })

  const defaultselectFilters= {
      mapscale:mainFilters.value.mapscale[0] ,
      district:[],
      regions: [],
      call_duration: mainFilters.value.call_duration[0],
      call_type: mainFilters.value.call_type[0],
      call_time_msc: mainFilters.value.call_time_msc[0],
      period: {from:'',to:''},
      previous_period:{from:'',to:''},
      holiday: mainFilters.value.holiday[1].val,
      from_ekc: mainFilters.value.from_ekc[0].val,
      direction:[]
      // periodEnd: null


    }

  const defaultaddselectFilters={
        tno:[],
        department:'',
        person:'',
        indicator:[],
        level:addictFilters.value.level[0]

  }


const addSelectFilters = ref(JSON.parse(JSON.stringify(defaultaddselectFilters)))    

const selectFilters=ref(JSON.parse(JSON.stringify(defaultselectFilters)))

defaultperiod()

function clear_filters(){
  
  selectFilters.value=JSON.parse(JSON.stringify(defaultselectFilters))
  defaultperiod()

  
}
function  clear_add_filters (){
  addSelectFilters.value=JSON.parse(JSON.stringify(defaultaddselectFilters))
}
 
function clear_all_filters(){
  clear_add_filters()  
  clear_filters()

}



async function defaultperiod(){
  let res = await api.get('/atc/getdates')
  let dates= [new Date(res.data[1]), new Date(res.data[0])]
  
  
  selectFilters.value.period=  {'from':date.formatDate(dates[0], "DD.MM.YYYY"), to:date.formatDate(dates[1],"DD.MM.YYYY")}
  let days = moment(dates[1]).diff(moment(dates[0]), 'days');

  let from = moment(dates[0]).subtract(days,'days')
  let to = moment(dates[0]).subtract(1,'days')
 
  selectFilters.value.previous_period =  {'from':from.format("DD.MM.YYYY"), to:to.format("DD.MM.YYYY")}
 }


  async function getfilterquery(filter){
      
      let res = await api.get(`fns/filter/?q=${filter}`)
      if (filter=='call_type')  res.data.unshift({name:"Все", id:null})
      return res.data
    }

  async function  getmainfilter(storek){
    for (let [key, val] of Object.entries(storek)){
      if (val.length==0 || (key=='call_type' && val.length==1)){
        
       
          storek[key]= await getfilterquery(key)
         
        }
    
      }
   
    }
 
  const objectq = computed({
    get(){
      let searchob= {}
      
      for (let[key,val] of Object.entries(selectFilters.value)){
          if (['district','regions'].includes(key) && val.length>0){            
            searchob[key]=val.reduce((arr, el)=>[...arr, el.id],[])  
          
          }      
           
          else if(key=='period'){
           
            searchob['date_fixation__gte']= format_date_to_base(val.from)
            searchob['date_fixation__lte']= format_date_to_base(val.to)
          
          }
          else if(key=='previous_period'){
            searchob['pdate_fixation__gte']=format_date_to_base(val.from)
            searchob['pdate_fixation__lte']=format_date_to_base(val.to)
               
          }
          else if(['call_type','call_time_msc','mapscale'].includes(key)&& val.id!==null)
            {searchob[key]=val.id
          }

          else if(key=='call_duration' && val.id!==null)
          {
            let k= val.id==1?'call_duration__gt': key           
            searchob[k]=0
        }
          // else if(key=='call_time_msc' &&  val.id!==null) {
          //   searchob[key]=val.id
          // }
          // else if(key=='mapscale'){
          //   searchob[key]=val.id
          // }   
          else if(['holiday','from_ekc'].includes(key)){
            searchob[key]=val
          }   
         
          
        }
        return searchob
    }
  })



    
  const  prepare_to_query = computed({
    get(){
      let searchob= JSON.parse(JSON.stringify(objectq.value))

        if (searchob.mapscale==1 && 'regions' in searchob &&  searchob.regions.length>0){
          delete searchob.regions
        }
        else if(searchob.mapscale==2 && 'district' in searchob && searchob.district.length>0){
          delete searchob.district
        }
  
        return searchob
    }
  })
  






  function toggleOption(opt, key, multi){  

    if (multi==true){
      let ind = selectFilters.value[key].findIndex(e=>e.id==opt.id)
      if (ind==-1){
        selectFilters.value[key].push(opt)
      }else{
        selectFilters.value[key].splice(ind,1)
      }
    }
    else{
      selectFilters.value[key]=opt
    }
  }
  function   toggleaddOption(opt, key, multi){ 

    if (multi==true){
      let ind = addSelectFilters.value[key].findIndex(e=>e.id==opt.id)
      if (ind==-1){
   
        addSelectFilters.value[key].push(opt)
      }else{
        addSelectFilters.value[key].splice(ind,1)
      }
    }
    else{
      addSelectFilters.value[key]=opt
    }
  }
  


  function changedata(whato_to_filt, nostorefilter={}){
   

    return api.post('/atc/getinfo/',{funct:whato_to_filt,
      
                                                 filters: {...prepare_to_query.value, ...nostorefilter }},
                                                 
                                                 {signal: apicontroller.value.signal,}
                                                 
                                                 )





  }

  const storefilters=computed({

    get(){
        for (let[key,val] of Object.entries({})){
          // Сюда пихнуть фильтра
        }


      return {}
    }




  })



  async function getaddfiltersq(filter,start){
      
      let res = await api.get(`fns/filter/?q=${filter}`)
      return res.data
  }

  async function  getaddfilters(storek){
   
    for (let [key, val] of Object.entries(storek)){
      if (val.length==0 && !(['department','person'].includes(key)) ){
        storek[key]= await getaddfiltersq(key,0)
      }
      // else{
      //   console.log(key);
      // }
    }
    if(addSelectFilters.value.level.id<3){
      addSelectFilters.value.level = addictFilters.value.level.find(
        (e) => e.id == selectFilters.value.mapscale.id
      );
      }
      if(tnofake.value!==null){
        addSelectFilters.value.tno=[addictFilters.value.tno.find(e=>e.id==tnofake.value)]
        tnofake.value=null
      }
    
  }

  getmainfilter(mainFilters.value)

function mainfiltersdetalize(sublevel,row){
  
  let filters = {}
  let level=''
  let indicator=[]
  

      
      
      if(Object.keys(row).length>0){
        
        indicator=addSelectFilters.value.indicator.sort((a,b)=>{return a.id-b.id}).reduce((arr,el)=>[...arr,el.field],[])
        for (let [key,val] of Object.entries(objectq.value)){
          if(['date_fixation__gte', 'date_fixation__lte'].includes(key)){
            filters[key]=val
        }
      }
          if(sublevel==0){
          
           
           
            level = addSelectFilters.value.level}
        

          else{
            level=addictFilters.value.level.find(e=>e.id==sublevel).level       
      
            let keystobase = {
              district_id:'district_id__in',
              ufns_id:'ufns_id__in',
              tno_id:'tno_id__in',
              deps_id: 'department_id',
              sub_b_id:'subscriber_b'
            }
            let clear = ['ufns_id','tno_id','deps_id','sub_b_id']
            for (let i=2; i<6;i++){
              if (sublevel<i) delete keystobase[clear[i-2]]
            }
            

           
            for(let x of Object.keys(keystobase )){             
              if (x in row){
               filters[keystobase[x]]=keystobase[x].endsWith('__in')? [row[x]]:row[x];
              }
            }
           

            

          }
        

      }   
    
      for (let [key,val] of Object.entries(addSelectFilters.value)){
        if(key=='tno' && val.length>0){
          filters['tno_id__in'] = val.reduce((arr, el)=>[...arr, el.id],[])
        }
        else if(key=='department' && val.length>0){

          filters['department__deps_name__icontains']=val
        }
      
        else if(key=='person'&& !!val && val.length>0){
          filters['subscriber_b__sn__icontains']=val
        }       

        else if(key=='level'){
          if (sublevel==0){
            level = val.level
           
          }
          else{
              
              level=addictFilters.value.level.find(e=>e.id==sublevel).level
          }
          

        }
        else if(key=='indicator' && val.length>0){
          indicator=val.sort((a,b)=>{return a.id-b.id}).reduce((arr,el)=>[...arr,el.field],[])
        

        }      
    }
      for (let [key,val] of Object.entries(objectq.value)){

        if (key=='district'){
            filters['district_id__in']=val
        }
        else if(key=='regions'){
          filters['ufns_id__in']=val
        }
        else if(['date_fixation__gte', 'date_fixation__lte','holiday','from_ekc'].includes(key)){
          filters[key]=val
        }
        else if(['call_type','call_time_msc'].includes(key)&& val!==null)
        {filters[key]=val
      }
      
       

      }

  return {filters,level, indicator}
}
const apicontroller_breaker=(loadingobject)=>{
  if(Object.values(loadingobject).some(e=>e==true)){
    apicontroller.value.abort()
  apicontroller.value = new AbortController();
  }
}

const avgmapView=ref(false)
const loadPerson = ref(false)
const tnofake=ref(null)
return {percenterview, tnofake,avgmapView,clear_add_filters, clear_filters,clear_all_filters, getmainfilter,addictFilters, mainFilters, selectFilters, toggleOption, prepare_to_query, changedata, 
  addSelectFilters,getaddfilters,getaddfilters, toggleaddOption,objectq,mainfiltersdetalize, loadPerson,apicontroller_breaker
}

});



