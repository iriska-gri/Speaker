<template>
  <div class="row q-gutter-x-xs no-wrap justify-between">
    
    <q-btn no-caps class="col q-pa-none "
    :ripple="{ color: ripplecolor[i] }" 
    :class="  globalx==i?$q.dark.isActive ?`bg-${ripplecolor[i]}-5`:`bg-${ripplecolor[i]}-2`:''"
    size="xs" v-for="(x, i) in calcdata" :key="i" @click="changemap(i)">
      <!-- <q-btn size="xs" no-caps class="col row cursor-pointer " @click="changemap(i)"
        
      
      > -->
      
        <div class="col text-center q-pa-xs  column ">
          <div class="col-auto text-subtitle2 ">{{ labels[0][i] }}  
          
          
          </div>
         
          <div class="col text-subtitle2">
            <div v-if="i == 'total'" >
              <span> 
              <NumberAnimate :total="x"/>
              
                <q-icon v-if="calcprevious[i]!=x" class="q-px-xs q-pt-xs cursor-pointer absolute-bottom-right"
                 :name="calcprevious[i]>x?'mdi-arrow-down-bold-circle-outline':'mdi-arrow-up-bold-circle-outline'"
                :color="colorer(i,x,calcprevious[i])"
                size="xs"
                >
              <q-tooltip>
                <div>Количество звонков:</div>               
                <div>В прошлом периоде: {{ calcprevious[i].toLocaleString("ru-RU") }}</div>
                <div>Изменение: {{ (x-calcprevious[i]).toLocaleString("ru-RU") }}</div>
              </q-tooltip>
              </q-icon>
             
              </span>
            </div>
            <div v-else-if="i == 'loadPerson'">
              <span>
                <NumberAnimate formatF= 'Percent' :total="x"/>%
                
              </span>
            </div>
            <div v-else-if="['accepted', 'missed', ].includes(i)">
              <span><NumberAnimate formatF= 'Percent' :total="x"/>% (<NumberAnimate :total="agregateData[i]"/>)
              
                  <q-icon v-if="calcprevious[i]!=x" 
                  class="q-px-xs q-py-xs cursor-pointer absolute-bottom-right"
                          :name="`mdi-arrow-${calcprevious[i]>x?'down':'up'}-bold-circle-outline`"
                          :color="colorer(i,x,calcprevious[i])"
                          size="xs"
                    >
                  <q-tooltip>         
                    <div>{{labels[0][i]}}</div>              
                    <div>В прошлом периоде: {{ calcprevious[i].toFixed(2).toLocaleString("ru-RU") }}%</div>
                    <div>Изменение: {{ (x-calcprevious[i]).toFixed(2).toLocaleString("ru-RU") }} %</div>
                  </q-tooltip>
                  </q-icon>
                  
              </span>
            </div>
           <div v-else-if="i == 'avg'">
            <span>
            <NumberAnimate  formatF="Date" :total="x"/>
           
                  <q-icon v-if="calcprevious[i]!=x" 
                          class="q-px-xs q-py-xs cursor-pointer absolute-bottom-right"
                          :name="`mdi-arrow-${calcprevious[i]>x?'down':'up'}-bold-circle-outline`"
                          :color="colorer(i,x,calcprevious[i])"
                          size="xs"
                    >
                  <q-tooltip>         
                    <div>{{labels[0][i]}}</div>   
                               
                    <div>В прошлом периоде: {{ momenter(calcprevious[i])}}</div>
                    <div>Изменение: {{ momenter((x-calcprevious[i])) }} </div>
                  </q-tooltip>
                  </q-icon>
                  

          </span>
          </div>
            <!-- <span v-if="['accepted', 'missed'].includes(i)"> 
              
            </span> -->
          </div>
        </div>
      <!-- </q-btn> -->
    </q-btn>
  </div>
</template>

<script>
import moment from "moment";
import { computed, ref } from "vue";
import { useQuasar } from "quasar";
import NumberAnimate from "../UI/NumberAnimate.vue";
import { useFilterStore } from "stores/filter-store.js";
export default {
  components: {
    NumberAnimate,
  },
  name:'IndicatorsCalls',
  props: {
    maindata: {
      type: Object,
      default: () => {
        return { total: 0, accepted: 0, missed: 0, avg: 0 };
      },
      
    },
    previousdata:{
      type: Object,
      default: () => {
        return { total: 0, accepted: 0, missed: 0, avg: 0 };
      },
      
    },
  },
  setup(props, { emit }) {
    const $q = useQuasar();
    moment.locale("ru");
    const worktime = 60 * 60 * 8
    const filterStore = useFilterStore();
    const labels = [
      {
        total: "Всего",
        accepted: "Принятых",    
        avg: "Средняя длительность",
        loadPerson: "Нагрузка на сотрудника",    
        // missed: "Пропущенных",
        // dropped:"Сброшенных"
      },
    ];
  const momenter=(val)=>{
    return  moment.unix(val, 2).utc().format("m мин ss сек")
  }
   

    const datacalcer = (data)=>{
      return {
          total: data.total,
          avg: data.avg / data.accepted,
          accepted: data.accepted*100 / data.total,
          loadPerson: data.callsum / (data.personsday * worktime ) * 100,
          // missed: data.missed * 100 / data.total,
          // dropped:data.dropped*100/data.total
        }
    }

    const calcdata = computed({
      get() {
        return datacalcer(agregateData.value)
         
      },
    });
    const calcprevious =  computed({
      get() {
        return datacalcer(agregateDataprevious.value)
         
      },
    });

    const aggregator=(data)=>{
      let tabdata = { total: 0, avg: 0, accepted: 0, persons: 0, personsday: 0, callsum: 0 };
        for (let x of data) {
          tabdata.total += x.total;
          tabdata.avg += parseFloat(x.avg) * (x.accepted);
          // tabdata.avgLoadPerson += x.callsum / (x.persons + x.personsday),
          tabdata.persons += x.persons
          tabdata.personsday += x.personsday
          tabdata.callsum += x.callsum
          tabdata.accepted += x.accepted
          // tabdata.missed += x.missed;
          // tabdata.dropped += x.dropped
        } 
        return tabdata
    }

    const agregateDataprevious = computed({
      get() {      
       
        return aggregator(props.previousdata)
      }
    })

    const agregateData = computed({
      get() {
               
        return aggregator(props.maindata)
      }
    })
    const colorer = (key, val,prev)=>{
      let grow = val>prev
      
      if (['missed','avg'].includes(key)){

        return grow?'red':'green'
      }
      else if(key=='accepted'){
       
        return grow?'green':'red'
      }
      return 'red'

    }
    const changemap=(key)=>
    {
      globalx.value=key
      
      if(['avg','loadPerson'].includes(key)){
        if (key=='avg'){
          filterStore.avgmapView=true
          filterStore.loadPerson=false
        } else {
          filterStore.avgmapView=false
          filterStore.loadPerson=true
        }
        filterStore.selectFilters.call_duration=filterStore.mainFilters.call_duration.find(r=>r.id===null)

      } else {
        
        filterStore.avgmapView=false
        filterStore.loadPerson=false
      let ind = filterStore.mainFilters.call_duration.findIndex(e=>e.field==key)
      if (ind>-1) {
        filterStore.selectFilters.call_duration=filterStore.mainFilters.call_duration[ind]
      }
      }
      console.log(labels);
      emit("changemapval",{v:labels[0][globalx.value],k:globalx.value=='accepted'?'accepted_p':globalx.value})
    }

    const ripplecolor={
      accepted:'green',
      loadPerson:'deep-orange',
      // missed: 'red',
      // dropped:'brown',
      total:'blue',
      avg:'deep-purple'
    }
    const globalx=ref('total')
    return {globalx,changemap, calcdata, labels, agregateData,calcprevious, agregateDataprevious, colorer, momenter,ripplecolor};
  },
};
</script>

<style></style>
