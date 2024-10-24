<template>
  <div>
    <div class="text-weight-bold text-caption text-no-wrap">
      {{ title }}
    </div>
      <q-input class="custom-cursor" dense="dense" outlined v-model="date" mask="##.##.####-##.##.####">
        <template v-slot:append>
          <q-icon name="event" class="cursor-pointer">
            <q-popup-proxy
              cover
              transition-show="scale"
              transition-hide="scale"
            >
          
              <q-date v-model="datepicker" range mask="DD.MM.YYYY">
                <div class="row items-center justify-end">

                  <q-btn v-close-popup label="Закрыть" color="primary" flat />
                </div>
              </q-date>
        
            </q-popup-proxy>
          </q-icon>
        </template>
      </q-input>
    
  </div>
</template>

<script>
import { ref, computed } from "vue";
import { useFilterStore } from "stores/filter-store.js";

export default {
  props: {
    title: {
      type: String,
      default: "Заголовок",
    },
    index:{
      type: Number,
      default:0
    }
  },
  setup(props) {
    
    const filterStore = useFilterStore();    
    const datepicker = computed({
      get(){
        return filterStore.selectFilters[props.index==0?'period':'previous_period']
      },
      set(val){
      
        if (val!==null)
{    filterStore.selectFilters[props.index==0?'period':'previous_period']=val}
      }
    })
    const date = computed({
      get(){
        
        let data = filterStore.selectFilters[props.index==0?'period':'previous_period']
        return `${data.from}-${data.to}`
      },
      set(val){
        
        try{
        let spltd = val.split('-')
        if (spltd.length==2)
        {filterStore.selectFilters[props.index==0?'period':'previous_period']={from:spltd[0],to:spltd[1]}}
        }catch{}
      
      
      }
    })  
    return {
      date,
      filterStore,
      datepicker
    };
  },
};
</script>

<style>
.custom-cursor .q-field__native {
  cursor: default; /* Изменяет курсор на указатель */
}
</style>
