<template>
       
  <q-page class="row q-col-gutter-y-xs no-scroll">
    <div class="col column q-px-sm q-col-gutter-y-xs">
      
      <div
        class="col-10 row q-col-gutter-x-xs"
        :class="$q.screen.lt.lg ? 'col-6' : ''"
      >

        <div
          class="col-lg-8 col-sm-3 full-height column q-col-gutter-y-xs"
          :class="$q.screen.lt.lg ? ' ' : ''"
        >

          <div class="col" >
         
            <MapRussia :loading="loading.maprussia" 
                      :indicator="graphdata.topandavg"
                      :maindata="graphdata.maprussia"
                       :recall="graphdata.recall" 
                      :previoustopavg="graphdata.previoustopavg"/>
          </div>
     
        </div>
        <div class="col-lg-2 col-sm-6 column full-height q-col-gutter-y-xs">
          <div :class="`col-${index==2?2:6}`" v-for="(x, index) in chartbars.leftside" :key="index">
            <q-card flat class="fit column" > 
              <div  style="place-content: space-between" class="q-pa-xs  row q-px-sm">
     
                <div class="column col-10 q-pa-none">
                  <div class=" q-pa-none col cursor-pointer text-caption" @click="openModal(x,index,'leftside')">
                  {{ x.data.shortdata.name }}
          
                </div>
                <div class="col  q-pa-none cursor-pointer text-caption " @click="openModal(x,index,'leftside')">
             
                  {{ x.data.shortdata.namefull }}
                </div>
                </div>
         
              </div>
      
              <div class="col">
                <q-skeleton v-if="x.loading" class="fit" />
                <component class="q-px-xs" v-else :is="x.component" :objData="x.data.shortdata" :clickable="false"/>
               
              </div>
            </q-card>
          </div>
        
       
        </div>
        <div class="col-lg-2 col-sm-3 column full-height q-col-gutter-y-xs">

          <div  :class="`col-${index==2?2:6}`" v-for="(x, index) in chartbars.rightside" :key="index">
            <q-card  flat class="fit column">           
              <q-card-section style="place-content: space-between" class="q-pa-xs text-body2 row q-px-sm">
                <div class="column col-10 q-pa-none">
                  <div class=" q-pa-none col cursor-pointer text-caption"  @click="openModal(x,index,'rightside')">
                  {{ x.data.shortdata.name }}
          
                </div>
                <div class="col  q-pa-none cursor-pointer text-caption "  @click="openModal(x,index,'rightside')">
             
                  {{ x.data.shortdata.namefull }}
                </div>
                </div>
                
              
              </q-card-section>
            
              <div class="col">
                <q-skeleton v-if="x.loading" class="fit" />
                <component class="q-px-xs" v-else :is="x.component" @directionfilter="directionfilter" :objData="x.data.shortdata" :clickable="true"/>
               
              </div>
            </q-card>
          </div>
       
       
        </div>
      </div>
      <div class="col-2 row q-pt-none q-col-gutter-x-xs">
        <!-- <div class="col column bg-red">
          <div class="bg-green col-12" v-for = "x in 4" :key=x>
                {{x}}
              </div>
        </div> -->
        <div class="col">
            <div class="row full-height">
             
              <div class="col-3" v-for="(x, index) in chartbars.bottom" :key="index" :class="index>0?'q-pl-xs':''">
                <!-- <q-card flat class="fit column" > -->
                  <q-skeleton v-if="x.loading" class="fit" />
                  <div class="row fit  " v-else>
                    <div class="col-2 text-caption text_line_hight  cursor-pointer" style="align-self: center"  @click="openModal(x,index,'bottom')">     {{ x.data.shortdata.name }}</div>
                    
                    <div class="col q-px-xs">
                       <component class=" q-px-md"  :is="x.component" :objData="x.data.shortdata" :clickable="false"/></div>
                      </div>
                      
                <!-- </q-card> -->
              </div>
            
            </div>
          </div>
      </div>
    </div>
    <q-dialog v-model="modelChart">
      <ui-modal :typeChar="openDialog" @directionfilter="directionfilter"  />

    </q-dialog>
  </q-page>
</template>

<script>
import ChartBar from "../components/dashboardpages/ChartBar.vue";
import ChartLine from "../components/dashboardpages/ChartLine.vue";


import MapRussia from "src/components/UI/MapRussia.vue";
import { useFilterStore } from "stores/filter-store.js";
import ChartLineDynamics from "../components/dashboardpages/ChartLineDynamics.vue";
import ChartBarDistribution from "../components/dashboardpages/ChartBarDistribution.vue";
import { ref, computed, watch } from "vue";
import { date } from "quasar";
import UiModal from "../components/UI/UiModal.vue";
// import { api, apicontroller, } from 'boot/axios'

export default {
  components: {
    // FilteredComp,
   
    ChartLine,
    ChartBar,
    MapRussia,
    ChartLineDynamics,
    ChartBarDistribution,
    UiModal,
  },
  setup() {

    const filterStore = useFilterStore();
    filterStore.clear_add_filters()
    const directionfilterarr=ref([])
    const modelChart = ref(false);
    const colors = {
        accepted:{active:{backgroundColor:"rgba(76,175,80,1)", borderColor:"rgba(56,142,60)"},
                  passive:{backgroundColor:"rgba(76,175,80,.4)",borderColor: "rgb(220,220,220)"}
        // passive:{backgroundColor:"rgba(183,28,28, 0.2)", borderColor:"rgba(183,28,28, 0.2))"}
      },
        missed: {active:{backgroundColor:"rgba(211,47,47,1)", borderColor:"rgba(211,47,47,1)"},
                    passive:{backgroundColor:"rgba(211,47,47,.4)",borderColor: "rgb(220,220,220)"}
                  // passive:{backgroundColor:"rgba(56,142,60, 0.2)", borderColor:"rgba(56,142,60)"}
                },
        dropped:{active:{backgroundColor:"rgba(109,76,65,1)", borderColor:"rgba(109,76,65,1)"},
        passive:{backgroundColor:"rgba(109,76,65,.4)", borderColor:"rgba(109,76,65,.4)"}
      },
        total:{active:{backgroundColor:"rgba(21,101,192,1)", borderColor:"rgba(21,101,192,1)",fill:'rgba(21,101,192, 0.2)'},passive:{backgroundColor:"rgba(21,101,192,1)", borderColor:"rgba(21,101,192,1)"}},
        placeholder:{active:{backgroundColor:"rgb(220,220,220)",borderColor: "rgb(220,220,220)"}},
        other:{active:{backgroundColor:"rgba(240,116,39,1)", borderColor:"rgba(240,116,39,1)",fill:'rgba(240,116,39,.2)'},passive:{backgroundColor:"rgba(21,101,192,1)", borderColor:"rgba(21,101,192,1)"}},
      }
    const graphdata = ref({      
      topandavg: [],
      previoustopavg:[],
      recall: [],
      maprussia: [],
      functionality: [],
      dynamic: [],
            
      timeclocker: [],
      incomemissed: [],
      
     
    });
    const loading = ref({
      topandavg: true,
      dynamic: true,
      functionality: true,
      recall: true,
      timeclocker: true,
      incomemissed: true,
      maprussia: true,
    });
    
    const graphplaceholder =(barThickness,backgroundColor)=>{return  [ {
            label: "",
            backgroundColor: backgroundColor,          
            data: [],
            barThickness: barThickness,
          },]}
    
    const topsDataorig = (colors,  name,barThickness=20) => {
    
      return {
        name:name[0],
        namefull: name[1],
        datasets: [
          {              
            backgroundColor: colors[0].backgroundColor,                   
            data: [],
            barThickness: barThickness,
          },
          {              
            backgroundColor: colors[2].backgroundColor,                   
            data: [],
            barThickness: barThickness,
          },
          ...graphplaceholder(barThickness,colors[1].backgroundColor),
         
        ],
        labels: [],      
        factdata: [],
      }}
    
    const dataprepare = (data, arr, accepted=true )=>{
      let ind= accepted==true?[0,2,1]:[2,0,1]
      data.labelsfull=[]
      let modif = "_p"
      let key=accepted==true?'accepted':'missed'
      let max=0
      if(!filterStore.percenterview){        
        modif = "" 
        data.datasets.push(  {              
            backgroundColor: 'white',                   
            data: [],
            barThickness: 20,
          },)
        max=Math.max(...arr.reduce((totalarr,elm)=>[...totalarr,elm.total],[]))     
      }  

      
      arr.forEach(e=>{      
        
        data.datasets[ind[0]].data.push(Math.round(e[`accepted${modif}`]*100)/100)
        data.datasets[ind[1]].data.push(Math.round(e[`missed${modif}`]*100)/100);
        data.datasets[ind[2]].data.push(Math.round(e[`dropped${modif}`]*100)/100);
        data.labels.push(e.name.replace("федеральный округ", "ФО"))
        data.accepted=accepted
        if(filterStore.percenterview){    
        data.factdata.push((accepted==true?[e.accepted,e.missed]:[e.missed,e.accepted ]))}
        else{
          data.datasets[3].data.push(max-e.total)
          data.factdata.push((accepted==true?[e.accepted_p,e.missed_p]:[e.missed_p,e.accepted_p ]))
        }
        data.labelsfull.push({name:e.name.replace("федеральный округ", "ФО"),id:e.id})
      })      
      
      return data
    }
    const dataprepare_functionality=(data, arr,color,accepted=true)=>{
      let max=0
        data.datasets.forEach(e=>{e.backgroundColor=[]})
          let modif = "_p"
       
        
      if(!filterStore.percenterview){        
        modif = ""  
        data.datasets.push(  {              
            backgroundColor: ['white'],                   
            data: [],
            barThickness: 20,
          },)
        max=Math.max(...arr.reduce((totalarr,elm)=>[...totalarr,elm.total],[]))         
      }  
        let ind= accepted==true?[0,2,1]:[2,0,1]
        data.labelsfull=[]
        let dirfilt = filterStore.selectFilters.direction.reduce((arra,el)=>[...arra, el.id],[])
        arr.forEach(e=>{
          let coltype = 'active'   
          // if(directionfilterarr.value.length>0 && !(directionfilterarr.value.includes(e.id))){  coltype='passive'  }
          if(filterStore.selectFilters.direction.length>0 && !(dirfilt.includes(e.id))){  coltype='passive'  }
            
          data.datasets[0].backgroundColor.push(color[coltype].backgroundColor)              
          data.datasets[1].backgroundColor.push(colors.placeholder.active.backgroundColor)
          data.datasets[2].backgroundColor.push(colors.placeholder.active.backgroundColor)

        if(filterStore.percenterview){    
          data.factdata.push((accepted==true?[e.accepted,e.missed]:[e.missed,e.accepted ]))}
          else{           
            data.datasets[3].data.push(max-e.total)
            data.factdata.push((accepted==true?[e.accepted_p,e.missed_p]:[e.missed_p,e.accepted_p ]))
          }

        data.datasets[ind[0]].data.push(Math.round(e[`accepted${modif}`]*100)/100)
        data.datasets[ind[1]].data.push(Math.round(e[`missed${modif}`]*100)/100);
        data.datasets[ind[2]].data.push(Math.round(e[`dropped${modif}`]*100)/100);
        data.labels.push(e.name)
      
        data.labelsfull.push({name:e.name,id:e.id})
      })    
        
      return data

    }






    const dataprepare_functionality_modal=(data, arr,color,accepted=true)=>{    
      let modif = "_p"
       
      let max=0  
      if(!filterStore.percenterview){        
        modif = ""  
        data.datasets.push(  {              
            backgroundColor: 'white',                   
            data: [],
            barThickness: 20,
          },)
        max=Math.max(...arr.reduce((totalarr,elm)=>[...totalarr,elm.total],[]))         
      }  
      

      let dirfilt = filterStore.selectFilters.direction.reduce((arra,el)=>[...arra, el.id],[])
      data.datasets.forEach(e=>{e.backgroundColor=[]})
        
      let ind= accepted==true?[0,2,1]:[2,0,1]
      data.labelsfull=[]
      arr.forEach(e=>{   
      let coltype = 'active'   
      if(filterStore.selectFilters.direction.length>0 && !(dirfilt.includes(e.id))){  coltype='passive'  }
        [0,1,2].forEach(n=>data.datasets[n].backgroundColor.push(colors[color[n]][coltype].backgroundColor)  )     
        
        


     
      if(filterStore.percenterview){    
          data.factdata.push((accepted==true?[e.accepted,e.missed]:[e.missed,e.accepted ]))}
          else{
            data.datasets[3].data.push(max-e.total)
            data.datasets[3].backgroundColor.push('white')
            data.factdata.push((accepted==true?[e.accepted_p,e.missed_p]:[e.missed_p,e.accepted_p ]))
          }
        data.datasets[ind[0]].data.push(Math.round(e[`accepted${modif}`]*100)/100)
        data.datasets[ind[1]].data.push(Math.round(e[`missed${modif}`]*100)/100);
        data.datasets[ind[2]].data.push(Math.round(e[`dropped${modif}`]*100)/100);
      
      data.labels.push(e.name)
      
      data.labelsfull.push({name:e.name,id:e.id})
    })    
      
    return data

  }


    const tops = computed({
      get() {
        let data = topsDataorig([colors.accepted.active, colors.placeholder.active, colors.placeholder.active], ["Территории."," ТОП-5 по принятым"],20 );
    
        let reverstops = graphdata.value.topandavg.slice()
        if(!filterStore.percenterview){        
        
        reverstops.sort((a,b)=>{return a.accepted-b.accepted})
      } 
        
        
       reverstops=reverstops.reverse().slice(0,5);
        data =  dataprepare(data, reverstops);
        
        data.clickable=true
        data.clickfunction = 'scalefilter'
        return data
      },
    });
    const topsModal = computed({
      get() {
        let data = topsDataorig([colors.accepted.active, colors.missed.active,colors.dropped.active], ["Территории. ТОП по принятым звонкам"],20);        
        let reverstops = graphdata.value.topandavg.slice().reverse();
        if(!filterStore.percenterview){ reverstops.sort((a,b)=>{return b.accepted-a.accepted})}
        data.clickfunction = null
        data.clickable=false
        data.modal=true
        data = dataprepare(data, reverstops)
       
        return data
      },
    });
    const tops_missedModal = computed({
      get() {
       
        let data = topsDataorig([colors.missed.active, colors.accepted.active,colors.dropped.active], ["Территории. ТОП по пропущенным звонкам"]);
        let reverstops = graphdata.value.topandavg.slice()
        if(!filterStore.percenterview){ reverstops.sort((a,b)=>{return b.missed-a.missed})
      } 
        data.clickable=false
        data.modal=true
        // data.clickfunction = 'scalefilter'
        data = dataprepare(data,reverstops, false)
        return data;
      },
    });
    

    const top_functionality = computed({
      get() {
        let data = topsDataorig([colors.accepted.active, colors.placeholder.active, colors.placeholder.active],["Направления.", "ТОП-5 по принятым"] );
        let reverstops = graphdata.value.functionality.slice().reverse()
        // console.log(graphdata.value.functionality);
        if(!filterStore.percenterview){ reverstops.sort((a,b)=>{return b.accepted-a.accepted})}
        
        reverstops=reverstops.slice(0,5);
        data= dataprepare_functionality(data, reverstops,colors.accepted);
        data.clickable=true        
        data.clickfunction = 'directionfilter'     
        return data
      },

    });

    const top_functionality_Modal = computed({
      get() {
        let data = topsDataorig([colors.accepted.active, colors.missed.active,colors.dropped.active],["Направления. ТОП по принятым звонкам"] );
        let reverstops = graphdata.value.functionality.slice().reverse();
        // data.size = { w: 1300, h: 750 };
        if(!filterStore.percenterview){ reverstops.sort((a,b)=>{return b.accepted-a.accepted})}
        data.modal=true
        data.clickable=true
        data.clickfunction = 'directionfilter'
        return  dataprepare_functionality_modal(data, reverstops, ['accepted','dropped','missed']);
      },
    });
    const anti_top_functionality = computed({
      get() {
        let data = topsDataorig([colors.missed.active, colors.accepted.active,colors.dropped.active],["Направления.", "ТОП-5 по пропущенным"] );
        let reverstops = graphdata.value.functionality.slice()
        if(!filterStore.percenterview){ reverstops.sort((a,b)=>{return b.missed-a.missed})}
        reverstops=reverstops.slice(0,5)  
        data=dataprepare_functionality(data, reverstops,colors.missed,false);
        data.clickable=true
        data.modal=false
        data.clickfunction = 'directionfilter'
        return data
      },
    });
    const anti_top_functionality_Modal = computed({
      get() {
        let data = topsDataorig([colors.missed.active, colors.accepted.active,colors.dropped.active], ["Направления. ТОП по пропущенным"] );
        let reverstops = graphdata.value.functionality.slice();
        // data.size = { w: 1300, h: 750 };
        if(!filterStore.percenterview){ reverstops.sort((a,b)=>{return b.missed-a.missed})}
        data.clickable=true
        data.modal=true
        data.clickfunction = 'directionfilter'
        return dataprepare_functionality_modal(data, reverstops, ['missed','dropped','accepted'], false);
      },
    });

   
    
    const tops_missed = computed({
      get() {
    
        let data = topsDataorig([colors.missed.active,colors.placeholder.active, colors.placeholder.active], ["Территории.", "ТОП-5 по пропущенным"]);  
        let reverstops = graphdata.value.topandavg.slice()
        if(!filterStore.percenterview){      
        
        reverstops.sort((a,b)=>{return b.missed-a.missed})
      }       
        reverstops = reverstops.slice(0,5)
        data = dataprepare(data, reverstops, false)
        data.clickable=true
        data.clickfunction = 'scalefilter'
        return data;
      },
    });

   

    const chartbars = computed({
      get(){return {leftside:[{ size:{ w: 1300, h: 500 },
                                component:'ChartBar' ,
                                loading:loading.value.topandavg,
                                data:{shortdata:tops.value, modal:topsModal.value }},
                              {
                                size:{ w: 1300, h: 500 },
                                loading:loading.value.topandavg,
                                component:'ChartBar' ,
                                data:{shortdata:tops_missed.value,modal:tops_missedModal.value}
                                                                                          
                              }
                              
                            
                            ],
                            topandavg: true,
     
   
     


                    rightside:[{ size:{ w: 1300, h: 500 },
                                component:'ChartBar' ,
                                loading:loading.value.functionality,
                                data:{shortdata:top_functionality.value, modal:top_functionality_Modal.value }},
                              {
                                size:{ w: 1300, h: 500 },
                                component:'ChartBar' ,
                                loading:loading.value.functionality,
                                data:{shortdata:anti_top_functionality.value,modal:anti_top_functionality_Modal.value}
                                                                                          
                              }
                             
                              
                            
                            ],
                  bottom:[
                             {
                                size:{ w: 1300, h: 700 },
                                loading:loading.value.recall,
                                component:'ChartLine' ,
                                data:{shortdata:recall.value, modal:recallModal.value}
                                
                                                            
                              },
                  
                  
                              { size:{ w: 1300, h: 700 },
                                component:'ChartLineDynamics' ,
                                loading:loading.value.incomemissed,
                                data:{shortdata:incomemissed.value, modal:incomemissedModal.value }},
                              {
                                size:{ w: 1300, h: 700 },
                                loading:loading.value.timeclocker,
                                component:'ChartBarDistribution' ,
                                data:{shortdata: timeclocker.value,modal:timeclockerModal.value}
                                                                                          
                              } ,
                              {
                                size:{ w: 1300, h: 700 },
                                loading:loading.value.dynamic,
                                component:'ChartLine' ,
                                data:{shortdata:dynamicCall.value, modal:dynamicCallModal.value}
                                
                                                            
                              },
                          
                            ]
                            
                            }}})



    const timeclocker = computed({
      get() {
        let data = {
          name: "Распределение звонков по часам",
          datasets: [
            {
              label: "Дозвон",
              hidden: false,
              backgroundColor: colors.accepted.active.backgroundColor,              
              data: [],
              barThickness: 11,
            },
            {
              label: "Сброс",
              hidden: false,
              backgroundColor: colors.dropped.active.backgroundColor,             
              data: [],
              barThickness: 11,
            },

            {
              label: "Недозвон",
              hidden: false,
              backgroundColor: colors.missed.active.backgroundColor,             
              data: [],
              barThickness: 11,
            },
            
          ],
          labels: [],
          type: "timeclocker",
        
          modal: false,
        };
        if(!filterStore.percenterview){
          // let sum


        graphdata.value.timeclocker.forEach((e) => {
          data.datasets[0].data.push(e.accepted);
          data.datasets[1].data.push(e.dropped);
          data.datasets[2].data.push(e.missed);
          data.labels.push(e.hour);
        })
        data.maxval=200
       }else{
          




          graphdata.value.timeclocker.forEach((e) => {
            let sum = [e.missed,e.accepted,e.dropped].reduce((s,el)=>s+el,0)
          data.datasets[0].data.push(Math.round(e.accepted*100/sum));
          data.datasets[1].data.push(Math.round(e.dropped*100/sum));
          data.datasets[2].data.push(Math.round(e.missed*100/sum));
          data.labels.push(e.hour);
        })
       }
        return data;
      },
    });

    const timeclockerModal = computed({
      get() {
        let data = JSON.parse(JSON.stringify(timeclocker.value));
        data.modal = true;        
        data.datasets.forEach((e) => (e.barThickness = 35));
        return data;
      },
    });

    const recall = computed({
      get() {
        let data = {
          name: "Динамика повторных звонков",
          datasets: [
            {
              label: "Повторные звонки, %",
              type:'bar',
              borderWidth: 1,
              pointRadius: 2,
              backgroundColor: colors.other.active.fill,
              borderColor: colors.other.active.backgroundColor,
              pointBackgroundColor: colors.other.active.backgroundColor,
              data: [],
              // fill: true,
              tooltip: {
              enabled: true,
              yAxisID: 'y',
              // callbacks: {
              //   label: function(value) {
              //     return `${value.formattedValue}%`
              //   },
              // },
    },
            },
            {
              label: "Повторные звонки, шт",
              yAxisID: 'y1',
              borderWidth: 2,
              pointRadius: 3,
              backgroundColor: colors.total.active.fill,
              borderColor: colors.total.active.backgroundColor,
              pointBackgroundColor: colors.total.active.backgroundColor,
              data: [],
              fill: false,              
    //           tooltip: {
    //           enabled: true,              
    //           callbacks: {
    //             label: function(value) {
    //               return `${value.formattedValue}шт`
    //             },
    //           },
    // },
            },

          ],
          labels: [],
          type: "recall",       
          modal: false,
        };

        graphdata.value.recall.forEach((e) => {
          data.datasets[1].data.push(e.recall)
          data.datasets[0].data.push(
            Math.round((e.recall * 100) / e.total)
          );
          data.labels.push(date.formatDate(e.day, "DD.MM.YYYY"));
        });

        return data;
      },
    });

    const recallModal = computed({
      get() {
        let data = JSON.parse(JSON.stringify(recall.value));
        data.modal = true;
        return data;
      },
    });

    const dynamicCall = computed({
      get() {
        let data = {
          name: "Динамика длительности звонков (сек)",
          datasets: [
            {
              label: "Ср. длительность звонков (сек)",
              borderWidth: 2,
              pointRadius: 3,
              backgroundColor: colors.total.active.backgroundColor,
              borderColor: colors.total.active.backgroundColor,
              pointBackgroundColor: colors.total.active.backgroundColor,
              data: [],
            },
          ],
          modal: false,
          labels: [],
          type: "dynamiccall",
          
        };

        graphdata.value.dynamic.forEach((e) => {
          if (e.call_timedelta_avg == null) data.datasets[0].data.push(0);
          else {
            data.datasets[0].data.push(Math.round(e.call_timedelta_avg));
          }

          data.labels.push(date.formatDate(e.day, "DD.MM.YYYY"));
        });
        return data;
      },
    });

    const dynamicCallModal = computed({
      get() {
        let data = JSON.parse(JSON.stringify(dynamicCall.value))
        data.modal = true;
        return data;
      },
    });

    const incomemissed = computed({
      get() {
        let data = {
          name: "Динамика принятых и пропущенных звонков",
          replay: [
            {
              label: "Пропущенные",
              data: [],
              // borderWidth: 2,
              pointRadius: 3,
              borderColor: colors.missed.active.borderColor,
              backgroundColor: colors.missed.active.backgroundColor,
              pointBackgroundColor: colors.missed.active.backgroundColor,
              hidden: true,
            },
            {
              label: "Принятые",
              data: [],            
              pointRadius: 3,
              borderColor: colors.accepted.active.backgroundColor,
              backgroundColor: colors.accepted.active.backgroundColor,
              pointBackgroundColor: colors.accepted.active.backgroundColor,
              hidden: true,
            },
            {
              label: "Сброшенные",
              data: [],              
              pointRadius: 3,
              borderColor: colors.dropped.active.backgroundColor,
              backgroundColor: colors.dropped.active.backgroundColor,
              pointBackgroundColor: colors.dropped.active.backgroundColor,
              hidden: true,
            },
            
          ],
          labels: [],
          type: "acceptmiss",
          size: { w: 1300, h: 450 },
          modal: false,
        };
        if(!filterStore.percenterview){
        data.replay.push({
              label: "Всего",
              data: [],              
              pointRadius: 3,
              borderColor: colors.total.active.backgroundColor,
              backgroundColor: colors.total.active.backgroundColor,
              pointBackgroundColor: colors.total.active.backgroundColor,
              hidden: true,
            })
          }
        graphdata.value.incomemissed.forEach((e) => {

          data.labels.push(date.formatDate(e.day, "DD.MM.YYYY"));
          if(!filterStore.percenterview){
          data.replay[0].data.push(e.missed);
          data.replay[1].data.push(e.accepted);
          data.replay[3].data.push(e.total);
          data.replay[2].data.push(e.dropped);}
          else{
            data.replay[0].data.push(Math.round(e.missed*100/e.total));
          data.replay[1].data.push(Math.round(e.accepted*100/e.total));
          // data.replay[2].data.push(100);
          data.replay[2].data.push(Math.round(e.dropped*100/e.total));
          }
        });
        if (filterStore.selectFilters.call_duration.id === null) {
          for (let i = 0; i < data.replay.length; i++) {
            data.replay[i].hidden = false;
          }
        } else if (filterStore.selectFilters.call_duration.id == 1) {
          data.replay[1].hidden = false;
          // data.replay[2].hidden = false;
        } else if (filterStore.selectFilters.call_duration.id == 2) {
          data.replay[0].hidden = false;
          // data.replay[2].hidden = false;
        }
        else if (filterStore.selectFilters.call_duration.id == 3) {
          data.replay[3].hidden = false;
          // data.replay[2].hidden = false;
        }
        // data.modal = false;
        return data;
      },
    });
    const oldstore = ref(JSON.parse(JSON.stringify(filterStore.selectFilters)))
    const incomemissedModal = computed({
      get() {
        let data = JSON.parse(JSON.stringify(incomemissed.value));
        data.modal = true;
        return data;
      },
    });
    
    const worktime = 60 * 60 * 8

    const percenterdata = (data) => {
      data.forEach((e)=>{
        e.accepted=e.total-e.missed-e.dropped
        e.missed_p= e.missed*100/e.total
        e.dropped_p = e.dropped*100/e.total
        e.accepted_p = e.accepted*100/e.total
        e.loadPerson = e.callsum/(e.personsday * worktime) * 100
       
      }
      )      
      return data.sort((a,b)=>{return b.missed_p-a.missed_p})
    }    
   const updateval =  () => {
      
      oldstore.value = JSON.parse(JSON.stringify(filterStore.selectFilters))
      Object.keys(loading.value).forEach(e=> loading.value[e]=true) 
         
      let arr = Object.keys(graphdata.value)
      arr.splice(arr.indexOf('maprussia'),1)
      let prom=[]
      let now = new Date()
      // arr=['recall']

    
      for (let key of arr) {
        
        if (key=='topandavg'){

        filterStore.changedata(key).then((res)=>{
              graphdata.value[key]=percenterdata(res.data)
              if (graphdata.value[key].length>0 && 'region_id' in  graphdata.value[key][0]){              
                
                graphdata.value.maprussia =maprussiadataregions(graphdata.value[key])
                
            }else{
              graphdata.value.maprussia = graphdata.value[key]
            }  
            loading.value[key]=false
            loading.value.maprussia=false
            
            })
           
        }
        else if(['functionality','previoustopavg'].includes(key)){
          filterStore.changedata(key).then((res)=>{graphdata.value[key]=percenterdata(res.data)
            loading.value[key]=false
          })
          }
        else{
          filterStore.changedata(key).then((res)=>{graphdata.value[key]=res.data
            loading.value[key]=false
        })
        }

    }
    
     
      
    };

    watch(
      () => filterStore.selectFilters,
      (newValue, oldValue) => {
        let change = false
        // if (directionfilterarr.value.length>0){
        //   directionfilterarr.value=[]
        //   change=true
        // }
        
        
        for(let [key,val] of Object.entries(filterStore.selectFilters)){
          if (['call_time_msc','call_type','mapscale'].includes(key) && ( oldstore.value[key].id!==filterStore.selectFilters[key].id))
          {
            
              change=true
          }
       
          else if(['period'].includes(key) && (oldstore.value[key].from!==filterStore.selectFilters[key].from||oldstore.value[key].to!==filterStore.selectFilters[key].to)){
         
            change=true
          }
          else if(['district','regions'].includes(key) && ( 
                            oldstore.value[key].length!==filterStore.selectFilters[key].length||
                            (oldstore.value[key].length==1 && 1==filterStore.selectFilters[key].length && oldstore.value[key][0].id!=filterStore.selectFilters[key][0].id)
                            
                            )){
       
            change=true
          }
          else if(['holiday','from_ekc'].includes(key) && ( oldstore.value[key]!==filterStore.selectFilters[key])){
        
            change=true
          }

        }
        // console.log(change);
        if(change==true){
          filterStore.apicontroller_breaker(loading.value)
          
          updateval()
        }
      
      },
      { deep: true }
    );
    
    watch(
      () => filterStore.selectFilters.previous_period,async (newValue, oldValue) => {
        if(oldstore.value.previous_period.from!==filterStore.selectFilters.previous_period.from||oldstore.value.previous_period.to!==filterStore.selectFilters.previous_period.to){
          oldstore.value = JSON.parse(JSON.stringify(filterStore.selectFilters))
          filterStore.apicontroller_breaker(loading.value)
          graphdata.value.previoustopavg = percenterdata(await filterStore.changedata('previoustopavg'));
        }
      }
      )

    watch(()=>filterStore.selectFilters.direction
      ,async()=>{
          console.log("sdlkjhlk");
        filterStore.apicontroller_breaker(loading.value)

      
Object.keys(loading.value).forEach((e)=> {if(e!='functionality'){loading.value[e]=true}}) 
let nf = filterStore.selectFilters.direction.length>0?{depdirection__in: filterStore.selectFilters.direction.reduce((arr,ell)=>[...arr,ell.id],[])}:{}
let arr = Object.keys(graphdata.value)
arr.splice(arr.indexOf('functionality'),1)
arr.splice(arr.indexOf('maprussia'),1)
for (let key of arr ){
  graphdata.value[key]=[]
 
  try {
    let r = await filterStore.changedata(key, nf)
    graphdata.value[key] = r.data;
    
    if (['topandavg','functionality','previoustopavg'].includes(key)){
      graphdata.value[key]=percenterdata(graphdata.value[key])
    }
    if (key=='topandavg'){            
      if (graphdata.value[key].length>0 && 'region_id' in  graphdata.value[key][0]){              
          
          graphdata.value.maprussia =maprussiadataregions(graphdata.value[key])
          loading.value.maprussia=false
      }else{
        graphdata.value.maprussia = graphdata.value[key]
        loading.value.maprussia=false
      }
    }
    loading.value[key]=false
 
  } catch(e) {
    console.log("qerror",e)
  }
}
if(modelChart.value == true)  openDialog.value.data = chartbars.value[openDialog.value.keyside][openDialog.value.indexside].data.modal




      },{deep:true}

    )




    const openDialog = ref();
    
    const openModal = (val, index, key) => {
      modelChart.value = true;

      openDialog.value = {data: val.data.modal,
                          indexside:index,
                          keyside:key,
                          component:val.component,
                           size:val.size} ;
     
    };
    const maprussiadataregions = (data)=>{
      let arr = JSON.parse(JSON.stringify(data))
                arr.forEach((e)=>{e.id=e.region_id
                  delete e.region_id
                })
      return arr
    }
    const directionfilter = async (val)=>{
      if (filterStore.selectFilters.direction.length>0){
      let indstore= filterStore.selectFilters.direction.findIndex(e=>e.id==val)
      if(indstore==-1){
        filterStore.selectFilters.direction.push(filterStore.mainFilters.direction.find(e=>e.id==val))
      }else{
        filterStore.selectFilters.direction.splice(indstore,1)
      }}
      else{
        filterStore.selectFilters.direction.push(filterStore.mainFilters.direction.find(e=>e.id==val))
      }
    

    }

    if (Object.values(filterStore.selectFilters.period).every(e=>e.length>0) ){
    
      directionfilterarr.value=[]
      updateval();
    }
   
    return {
      chartbars,
      directionfilter,
      graphdata,
    
    
      modelChart,
      openModal,
      openDialog,
     
      loading,

  
    };
  },
};
</script>

<style scoped>
canvas {
  width: 100% !important;
  height: 100% !important;
}
</style>
