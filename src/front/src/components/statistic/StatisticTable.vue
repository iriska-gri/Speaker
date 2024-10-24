<template>
  <div class="column q-px-sm col-12">
    <div class="col-auto">
      <q-breadcrumbs class="text-caption">
        <q-breadcrumbs-el class="cursor-pointer" v-for="x in breader" 
                                                        :key="x.label" 
                                                        :label="x.label"
                                                         @click="subdatagetter(x.filtr)" > </q-breadcrumbs-el>
      </q-breadcrumbs>
    </div>
    <div class="col" ref="columnsel">
    
      <q-table
        class="fit hoverRed"
      
        :class="$q.dark.isActive ? 'darkhead ' : ''"
        binary-state-sort
      @virtual-scroll="onScroll"
        :style="`max-height: ${!!columnsel ? columnsel.clientHeight : 100}px`"
        flat
        bordered
        dense
        wrap-cells
        :rows="tabledata"
        :columns="columns"
        row-key="name"
        separator="cell"
        :rows-per-page-options="[100,200,300,500,1000]"
        :loading="loading"
        :visible-columns="visiblercolumns"
      >
        <template v-slot:loading>
          <q-inner-loading showing>
            <q-circular-progress
              indeterminate
              rounded
              size="100px"
              color="blue-8"
              class="q-ma-md"
              :thickness="0.07"
            />
          </q-inner-loading>
        </template>
        <template v-slot:body-cell-index="props">
          <q-td>{{ props.rowIndex +1 }}</q-td>
        </template>
        <template v-slot:body-cell-district="props">
          <q-td class="cursor-pointer hovered"
           
            :props="props"
            @click="subdatagetter({ sublevel: 1, row: props.row })"
          >
            {{ props.value }}
          </q-td>
        </template>
        <template v-slot:body-cell-region="props">
          <q-td class="cursor-pointer hovered"
            :props="props"
            @click="subdatagetter({ sublevel: 2, row: props.row })"
          >
            {{ props.value }}
          </q-td>
        </template>
        <template v-slot:body-cell-tno="props">
          <q-td class="cursor-pointer hovered"
            :props="props"
            @click="subdatagetter({ sublevel: 3, row: props.row })"
          >
            {{ props.value }}
          </q-td>
        </template>
        <template v-slot:body-cell-department="props">
          <q-td class="cursor-pointer hovered"
            :props="props"
            @click="subdatagetter({ sublevel: 4, row: props.row })"
          >
            {{ props.value }}
          </q-td>
        </template>
        <template v-slot:body-cell-person="props">
          <q-td class="cursor-pointer hovered"
            :props="props"
            @click="subdatagetter({ sublevel: 5, row: props.row })"
          >
            <span
              :class="
                'disabled' in props.row &&
                props.row.disabled == true &&
                date.addToDate(new Date(props.row.pwd_lastset), {
                  months: 1,
                }) <= filterStore.objectq.date_fixation__lte &&
                date.addToDate(new Date(props.row.pwd_lastset), {
                  months: 1,
                }) >= filterStore.objectq.date_fixation__gte
                  ? 'text-red'
                  : ''
              "
            >
              {{ props.value }}</span
            >
          </q-td>
        </template>
      
        <template v-slot:header="props" >
          
        <q-tr :props="props" id="header" >
          <q-th
            v-for="col in props.cols"
            :key="col.name"
            :props="props"
            class=""
          >          
            {{ col.label }}
          </q-th>
          
        </q-tr>
       
      </template>
      
      <template v-slot:top-row >
        <q-tr 
        v-if="visiblercolumns.some(e=>Object.keys(avgcalculatedresult).includes(e))"
        :class="loading?'disabled':$q.dark.isActive ? 'bg-dark' : ''"
        
          class="text-weight-bold text-h4 text-blue-14 non-selectable"
         :style="`background-color:white; position:sticky; z-index:1;top:${headertop}px`"> 
        <q-td  :colspan="avgcolspan" class=" text-right">Среднероссийские показатели</q-td>
        <!-- <q-td >{{ avgcalculated }}</q-td> -->
        <q-td v-for="x,index in addcolumns.filter(els=>visiblercolumns.includes(els.name))"  :key="index" class="text-right" :class="x.name == toBgColor ? 'bgBlue' : ''">
         
        <span v-if="x.name in avgcalculatedresult &&  visiblercolumns.includes(x.name)"  >{{ avgcalculatedresult[x.name] }}</span>
        
        </q-td>
        </q-tr>
      </template>
     
        <template v-slot:body-cell-countcalls="props">
          <q-td :props="props" class=" non-selectable" 
          :class="$q.dark.isActive ? 'bg-grey' : 'bg-grey-3'"
          @mouseover="toBgColor = props.col.name" @mouseleave="toBgColor = null">
            {{ !!props.value?props.value.toLocaleString("ru-RU"):"" }}
          </q-td>
        </template>
        <template v-slot:body-cell-dropped_p="props">
          <q-td :props="props"  :class="colorer(props.value,'dropped_p',colored_p_dropped)" class="non-selectable" @mouseover="toBgColor = props.col.name" @mouseleave="toBgColor = null">
          
            {{!!props.value? parseFloat(props.value.toFixed(2)):"" }}
          </q-td>
         
        </template>
        <template v-slot:body-cell-dropped="props">
          <q-td :props="props"  :class="colorer(props.value,'dropped_p',colored_dropped)" class="non-selectable" @mouseover="toBgColor = props.col.name" @mouseleave="toBgColor = null">
          
            {{ !!props.value?props.value.toLocaleString("ru-RU"):"" }}
          </q-td>
         
        </template>


        <template v-slot:body-cell-accepted_p="props">
          <q-td :props="props"   :class="colorer(props.value,'accepted_p',colored_p_accepted)" class="non-selectable" @mouseover="toBgColor = props.col.name" @mouseleave="toBgColor = null">            
            {{ !!props.value?props.value:'' }}           
          </q-td>
        </template>
        <template v-slot:body-cell-accepted="props">
          <q-td :props="props"   :class="colorer(props.value,'accepted',colored_accepted)" class="non-selectable" @mouseover="toBgColor = props.col.name" @mouseleave="toBgColor = null">            
            {{ !!props.value?props.value.toLocaleString("ru-RU"):"" }}         
          </q-td>
        </template>
        <template v-slot:body-cell-missed_p="props">
          <q-td :props="props"  :class="colorer(props.value,'missed_p',colored_p_missed)" class="non-selectable" @mouseover="toBgColor = props.col.name" @mouseleave="toBgColor = null">
            <!-- :class="colorer(props.value,'missed',colored_p_missed)" -->
            {{ !!props.value?parseFloat(props.value.toFixed(2)):'' }} 
            <!-- ({{  !!props.value?props.row.missedcount.toLocaleString("ru-RU"):"" }})  -->
          </q-td>
        </template>
        <template v-slot:body-cell-missed="props">
          <q-td :props="props"   :class="colorer(props.value,'missed',colored_missed)" class="non-selectable" @mouseover="toBgColor = props.col.name" @mouseleave="toBgColor = null">            
            {{ !!props.value?props.value.toLocaleString("ru-RU"):"" }}          
          </q-td>
        </template>
        <template v-slot:body-cell-worktime="props" >
          <q-td :props="props" class="non-selectable" 
          :class="$q.dark.isActive ? 'bg-grey' : 'bg-grey-3'"
          @mouseover="toBgColor = props.col.name" @mouseleave="toBgColor = null">
            {{  !!props.value?props.value.toLocaleString("ru-RU"):'' }}
          </q-td>
        </template>
        <template v-slot:body-cell-nowork="props" >
          <q-td :props="props" class="non-selectable"
          :class="$q.dark.isActive ? 'bg-grey' : 'bg-grey-3'"
          @mouseover="toBgColor = props.col.name" @mouseleave="toBgColor = null">
            {{ !!props.value? props.value.toLocaleString("ru-RU"):'' }}
          </q-td>
        </template>
        <template v-slot:body-cell-avgtime="props" >

          <q-td :props="props" class=" non-selectable"
          :class="$q.dark.isActive ? 'bg-grey' : 'bg-grey-3'"
          @mouseover="toBgColor = props.col.name" @mouseleave="toBgColor = null">
        
            <!-- :class="colorer(props.value,'avgtime',colored_p_avgtime)" -->
            {{ !!props.value?props.value:'' }}
          </q-td>
        </template>
        <template v-slot:body-cell-personloading="props" >
          <q-td :props="props" :class="colorer(props.value,'personloading',personloading)" class="non-selectable" @mouseover="toBgColor = props.col.name" @mouseleave="toBgColor = null">
                 {{ !!props.value?props.value:'' }}
          </q-td>
        </template>
        
        <template v-slot:body-cell-countcalls_to_person="props">
          <q-td :props="props" :class="colorer(props.value,'countcalls_to_person',countcalls_to_person)" class="non-selectable" @mouseover="toBgColor = props.col.name" @mouseleave="toBgColor = null">
                 {{ !!props.value?props.value:'' }}
          </q-td>
        </template>

        <template v-slot:body-cell-callpeak="props" >
          <q-td :props="props" class="non-selectable"
          :class="$q.dark.isActive ? 'bg-grey' : 'bg-grey-3'"
          >
                 {{ !!props.value?props.value:'' }}
          </q-td>
        </template>

        

        <!-- <template v-slot:bottom>
            <q-table
              hide-header
              hide-bottom
              dense
              wrap-cells
              :rows="[avgrussia]"
              :columns="columns.addcolumns"
              separator="cell">
              
            </q-table>
        </template> -->
      </q-table>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted,onUpdated } from "vue";
import { useFilterStore } from "stores/filter-store.js";
import { date } from "quasar";
import { useQuasar } from 'quasar'
import moment from "moment";
export default {
  props: {
    loading: {
      type: Boolean,
      default: false,
    },

    tabledata: {
      type: Array,
      default: () => [],
    },
    addcolumns: {
      type: Array,
      default: () => [],
    },
   
    avgrussia:{
      type: Object,
      default: () => {return {
        
        missed: 0,
        
       total:0,
        worktime: 0,
        nowork: 0,
        avgtime:0,
        droppedcalc:  0,
        dropped: 0,
      }},
    }

  },
  setup(props, { emit }) {
    const columnsel = ref(null);
    const filterStore = useFilterStore();
    const header=ref(null)
    const headertop= ref(0)
    const $q = useQuasar()
    const toBgColor = ref(null)
    const colors = computed({get(){
     return {
     
      forward: $q.dark.isActive ?
              ['bg-red-10','bg-red-9','bg-red-8','bg-red-7','bg-green-7','bg-green-8','bg-green-9','bg-green-10']:
              ['bg-red-5','bg-red-4','bg-red-3','bg-red-2','bg-green-2','bg-green-3','bg-green-4','bg-green-5']
              ,

      backward:$q.dark.isActive ?['bg-green-10','bg-green-9','bg-green-8','bg-green-7','','bg-red-7','bg-red-8','bg-red-9','bg-red-10']:
      ['bg-green-5','bg-green-4','bg-green-3','bg-green-2','','bg-red-2','bg-red-3','bg-red-4','bg-red-5']
      // ['bg-red-5','bg-red-4','bg-red-3','bg-red-2','','bg-green-2','bg-green-3','bg-green-4','bg-green-5']
    }}})
    const colorsbase = computed({get(){
      return{
        accepted: colors.value.forward,
        accepted_p: colors.value.forward,
        missed: colors.value.backward,
        missed_p: colors.value.backward,
        avgtime:colors.value.forward,
        dropped:colors.value.backward,
        dropped_p:colors.value.backward,
        personloading:colors.value.backward,
        countcalls_to_person:colors.value.backward
      }    }})
    const colorer=(val,color, compf)=>{
      // console.log(val, color, compf);
      if (compf.length>0 && val){
      let i=0      
      while (i<colorsbase.value[color].length && val>=compf[i]) {
        
        i=i+1
      }
    
      return colorsbase.value[color][i]
    }
      return 'bg-grey'
   }
   
   const minmaxstep=(field)=>{
    
    let arr = props.tabledata.reduce((arr,e)=>[...arr,e[field]],[])
    
    let [min,max]=[Math.min(...arr),Math.max(...arr)]
    let tominstep=(avgcalculated.value[field]-min)/(colorsbase.value[field].length/2)
    let tomaxstep = (max-avgcalculated.value[field])/(colorsbase.value[field].length/2)
   
    let n=1
  
    let res = [avgcalculated.value[field]]
    
    while (n<(colorsbase.value[field].length-1)/2){
       
        res.push(avgcalculated.value[field]+(n*tomaxstep))
        res.unshift(avgcalculated.value[field]-(n*tominstep))
        n++
      
    }
   
    return res
   }
    
   const avgcalculated = computed({
    get(){
    
      return {
        countcalls:props.avgrussia.total/props.avgrussia.totalels,
        missed: props.avgrussia.missed/props.avgrussia.totalels,
        missed_p: props.avgrussia.missed*100/props.avgrussia.total,
        accepted:(props.avgrussia.total-props.avgrussia.missed-props.avgrussia.dropped)/props.avgrussia.totalels,
        accepted_p: (props.avgrussia.total-props.avgrussia.missed-props.avgrussia.dropped)*100/props.avgrussia.total,
        worktime: props.avgrussia.worktime/props.avgrussia.totalels,
        nowork: (props.avgrussia.total-props.avgrussia.worktime)/props.avgrussia.totalels,
        avgtime:props.avgrussia.avg_duration,
        dropped:  props.avgrussia.dropped/props.avgrussia.totalels,
        dropped_p:  (props.avgrussia.dropped)*100/props.avgrussia.total,
        personloading: props.avgrussia.personloading,
        countcalls_to_person:props.avgrussia.countcalls_to_person
        
        
      }
    }
   })
   const avgcalculatedresult = computed({
    get(){
        return {
                countcalls:Math.round(avgcalculated.value.countcalls).toLocaleString("ru-RU"),
                worktime:Math.round(avgcalculated.value.worktime).toLocaleString("ru-RU"),
                nowork:Math.round(avgcalculated.value.nowork).toLocaleString("ru-RU"),
                missed: Math.round(avgcalculated.value.missed).toLocaleString("ru-RU"),
                missed_p:avgcalculated.value.missed_p.toFixed(2),
                dropped:Math.round(avgcalculated.value.dropped).toLocaleString("ru-RU"),
                dropped_p:avgcalculated.value.dropped_p.toFixed(2),
                accepted: Math.round(avgcalculated.value.accepted).toLocaleString("ru-RU"),                
                accepted_p:`${avgcalculated.value.accepted_p.toFixed(2)}`,
                avgtime: moment.unix(Math.round(avgcalculated.value.avgtime)).format('m мин ss сек'),
                personloading: props.avgrussia.personloading?props.avgrussia.personloading.toFixed(2):'',
                countcalls_to_person:props.avgrussia.countcalls_to_person?Math.round(props.avgrussia.countcalls_to_person).toLocaleString("ru-RU"):''


    }   
    }})

   const colored_p_dropped=computed({
      get()
      {   
        
        if(props.tabledata.length>0 && props.addcolumns.reduce((arr,e)=>[...arr,e.field],[]).includes('dropped_p')){  
        return minmaxstep('dropped_p')
        }
        return 0
      }
    })
    const countcalls_to_person=computed({
      get()
      {   
        if(props.tabledata.length>0 && props.addcolumns.reduce((arr,e)=>[...arr,e.field],[]).includes('countcalls_to_person')){  
        return minmaxstep('countcalls_to_person')
        }
        return 0
      }
    })

    const personloading=computed({
      get()
      {   
        if(props.tabledata.length>0 && props.addcolumns.reduce((arr,e)=>[...arr,e.field],[]).includes('personloading')){  
        return minmaxstep('personloading')
        }
        return 0
      }
    })
    const colored_dropped=computed({
      get()
      {   
        if(props.tabledata.length>0 && props.addcolumns.reduce((arr,e)=>[...arr,e.field],[]).includes('dropped')){  
        return minmaxstep('dropped')
        }
        return 0
      }
    })




    const colored_p_missed=computed({
      get()
      {   
        if(props.tabledata.length>0 && props.addcolumns.reduce((arr,e)=>[...arr,e.field],[]).includes('missed_p')){  
        return minmaxstep('missed_p')
        }
        return 0
      }
    })

    const colored_missed=computed({
      get()
      {   
        if(props.tabledata.length>0 && props.addcolumns.reduce((arr,e)=>[...arr,e.field],[]).includes('missed')){  
        return minmaxstep('missed')
        }
        return 0
      }
    })
    const colored_p_accepted=computed({
      get()
      {   
      
        if(props.tabledata.length>0 && props.addcolumns.reduce((arr,e)=>[...arr,e.field],[]).includes('accepted_p')){  
        return minmaxstep('accepted_p')
        }
        return 0
      }
    })
    const colored_accepted=computed({
      get(){
        if(props.tabledata.length>0 && props.addcolumns.reduce((arr,e)=>[...arr,e.field],[]).includes('accepted')){  
        return minmaxstep('accepted')
        }
        return 0
      }
    })
   
    const colored_p_avgtime=computed({
      get()
      {   
        if(props.tabledata.length>0 && props.addcolumns.reduce((arr,e)=>[...arr,e.field],[]).includes('avgtime')){  
        return minmaxstep('avgtime')
        }
        return 0
      }
    })


    const columns = computed({
      get() {
        return [
          {
            align: "center",
            label: "#",
            name: "index",
            field: "index",
            style: "width: 2%",
            headerStyle: "width: 2%",
            // sortable: true,
          },
          {
            name: "district",
            required: true,
            label: props.tabledata.length>1?'Федеральные округа':"Федеральный округ",
            align: "left",
            field: "district",
            format: (val) => `${val.replace("федеральный округ", "")}`,

            sortable: true,
          },

          {
            align: "left",
            label: ["Регион","Регионы"][datareducer("region")],
            name: "region",
            field: "region",
            sortable: true,
          },
          {
            align: "left",
            label: ["Инспекция","Инспекции"][datareducer("tno")],
            name: "tno",
            field: "tno",
            sortable: true,
          },
          {
            align: "left",
            label: ["Отдел","Отделы"][datareducer("department")],
            name: "department",
            field: "department",
            sortable: true,
          },
          {
            align: "left",
            label: ["Сотрудник","Сотрудники"][datareducer("person")],
            name: "person",
            field: "person",
            sortable: true,
          },

          ...props.addcolumns,
          
        ];
      },
    });

    const datareducer = (key)=>{
      let res = 0
      if(props.tabledata.length>1){
        if(Number.isInteger(props.tabledata[0][key])){
          res=1
        }
        else{
          let s = new Set()
          props.tabledata.forEach(e=>s.add(e[key]))
          if (s.size>1){
            res=1
          }

        }
      
      
      }
      else if (props.tabledata.length==1 && Number.isInteger(props.tabledata[0][key]) && props.tabledata[0][key]>1){res=1}
      return res
      
    }


    const breadCrumbs = ref([]);

    const subdatagetter = (filtr) => {
      
      breadCrumbs.value=filtr;
     
      emit("getsubinfo", filtr);
    };
    
    const breader = computed({get()
     {
      let  breads = [{label:"Федеральные округа",filtr:{sublevel:1, row:{}}}]
      
  
      if(breadCrumbs.value.sublevel>=1 && props.tabledata.length>0){

        if (props.tabledata.length>=1 && props.tabledata.every(e=>e.district==props.tabledata[0].district)){ 
        
          breads.push({label:props.tabledata[0].district,filtr:{sublevel:1, row:breadCrumbs.value.row}})
        }
      }
      if(breadCrumbs.value.sublevel>=2 && props.tabledata.length>0){

        if (props.tabledata.length>1 && props.tabledata.some(e=>e.region!=props.tabledata[0].region)){ 
              breads.push({label:"Регионы",filtr:{sublevel:2, row:breadCrumbs.value.row}})
            }
            else if(Number.isInteger(props.tabledata[0].region)==false){
              breads.push({label:props.tabledata[0].region,filtr:{sublevel:2, row:breadCrumbs.value.row}})
            }
      }
      if(breadCrumbs.value.sublevel>=3 && props.tabledata.length>0){
  
        if (props.tabledata.length>1 && props.tabledata.some(e=>e.tno!=props.tabledata[0].tno)){ 
                breads.push({label:"Инспекции",filtr:{sublevel:3, row:breadCrumbs.value.row}})
              }
              else if(Number.isInteger(props.tabledata[0].tno)==false){
              breads.push({label:props.tabledata[0].tno, filtr:{sublevel:3, row:breadCrumbs.value.row}})
            }
         
      }
      if(breadCrumbs.value.sublevel>=4 && props.tabledata.length>0){
       
        if (props.tabledata.length>1 && props.tabledata.some(e=>e.department!=props.tabledata[0].department)){
               breads.push({label:"Отделы",filtr:{sublevel:4, row:breadCrumbs.value.row}})
              }
              else if(Number.isInteger(props.tabledata[0].department)==false){
                breads.push({label:props.tabledata[0].department,filtr:{sublevel:4, row:breadCrumbs.value.row}})
              }
       
      }
      if(breadCrumbs.value.sublevel>=5 && props.tabledata.length>0){
       
        if (props.tabledata.length>1 && props.tabledata.some(e=>e.person!=props.tabledata[0].person)){
               breads.push({label:"Сотрудники",filtr:{sublevel:5, row:breadCrumbs.value.row}})
              }
              else if(Number.isInteger(props.tabledata[0].person)==false){
                breads.push({label:props.tabledata[0].person,filtr:{sublevel:5, row:breadCrumbs.value.row}})
              }
       
      }
      

      return breads
     } 
      
    })
    const nextPage = ref(2)
    const onScroll=({to,ref})=>{

      // const lastIndex = props.tabledata.length - 1

      //   if (props.loading !== true && nextPage.value < props.lastPage && to === lastIndex) {
      //     // loading.value = true
      //       console.log("ssss");
      //     // setTimeout(() => {
      //     //   nextPage.value++
      //     //   nextTick(() => {
      //     //     ref.refresh()
      //     //     loading.value = false
      //     //   })
      //     // }, 500)

      //   }

    }
    const avgcolspan = computed({
      get(){
        // ['countcalls','worktime','nowork']
        // addcolumns
        let colspan=5
        // props.addcolumns.forEach((e)=> {if(['countcalls','worktime','nowork'].includes(e.field))
        // colspan+=1
          
        // })
        return colspan
      }
    })
    const headertopper=()=>{
      headertop.value=document.getElementById('header').clientHeight
    }
    const breads = ref();
    onMounted(() => {
      headertopper()
    })
    onUpdated(() => {
      headertopper()
    })
    watch(
      () => $q.screen.width,
      (newValue, oldValue) => {
        headertopper()
      }, {deep:true})

    const visiblercolumns=computed({
      get(){
       
        
        if(props.tabledata.length>0) return Object.keys(props.tabledata[0]).filter(e=>!e.endsWith("_id"))
        return []
      }
    })
     
    return {
      avgcolspan,
      avgcalculatedresult,
      headertop,
      header,
      avgcalculated,
      onScroll,
      colored_p_dropped,
      colored_dropped,
      colored_p_accepted,
      colored_accepted,
      colored_p_missed,
      colored_missed,
      colored_p_avgtime,
      colorer,
      breader,
      columns,
      subdatagetter,
      breads,
      filterStore,
      date,
      columnsel,
      breadCrumbs,
      personloading,
      countcalls_to_person,
      toBgColor,
      visiblercolumns
    };
  },
};
</script>
<style lang="scss">
/* height or max-height is important */

.q-table__top,

thead tr:first-child th {
  /* bg color is important for th; just specify one */
  background-color: white;
}
.darkhead tr:first-child th {
  /* bg color is important for th; just specify one */
  background-color: $dark;
}

// :class="$q.dark.isActive ? 'darkhead ' : ''"


thead tr th {
  position: sticky;
  z-index: 1;
  
}


thead  th {
  top: 0;
}

/* this is when the loading indicator appears */
.q-table--loading thead tr:last-child th
    /* height of all previous header rows */ {
  top: 0px;
}

/* prevent scrolling behind sticky top row on focus */
tbody
    /* height of all previous header rows */ {
  scroll-margin-top: 68px;
}

::-webkit-scrollbar {
  width: 0.5em;
  height: 0.5em;
}
::-webkit-scrollbar-thumb {
  background-color: var(--q-primary);
  border-radius: 3px;
  opacity: 1;
  width: 5px !important;
}

td.hovered:hover {
  background-color: rgba(68, 68, 68,.3);
  animation-name: slidein;
animation-duration: .5s;
animation-iteration-count: 1;
// animation-iteration-count: 2, 1, 5;
}
@keyframes slidein {
  from {
    background-color: rgba(255, 255, 255, 0.3);
  }

  to {
    background-color: rgba(68, 68, 68,.3);
  }
}

@keyframes alexTolltip {
  from {
    background-color: transparent;
  }
  to {
    background-color: #BBDEFB;
  }
}

.bgBlue {
  animation-fill-mode: forwards;
  animation-name: alexTolltip;
  animation-duration: .9s;
  animation-iteration-count: 1;
}
</style>