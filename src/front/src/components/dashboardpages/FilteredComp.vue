<template>
  <div class="row" >
    <div class="col row ">
      <div class="col row q-col-gutter-xs">
        <div class="col-auto column self-end q-col-gutter-xs ">
          <q-btn class="q-pa-none q-my-xs" 
          :icon="filterStore.selectFilters.mapscale.id==1?'mdi-earth-plus':'mdi-earth-minus'" 
          round flat padding="sm"
          @click="scalecjhanger"
          >
        <q-tooltip>Масштаб карты: {{ filterStore.selectFilters.mapscale.name }}</q-tooltip>
        </q-btn>
        </div>
       
      <div v-for="x in maindataSelectFilters" :key="x" :class="x.col" >
        <UIFilter
          :title="x.title"
          :label="x.label"
          :multi="x.multi"
          :storekey="x.storekey"
        />
      </div>
      <div class="col-3 row q-col-gutter-xs">
      <div
        class="col-6"
        v-for="(x, index) in ['Текущий период','Сравниваемый период']"
        :key="x"
      >
      <UIDateSelect :title="x" :index="index" />
    </div>
      </div>
      <div class="col-2 row ">
      <div class="col-6 column self-end q-col-gutter-xs ">
          <q-toggle 
            class="text-caption" 
            dense 
            size="xs"
          
            toggle-indeterminate
            v-model="filterStore.selectFilters.from_ekc"           
            :label="filterStore.mainFilters.from_ekc.find(e => e.val == filterStore.selectFilters.from_ekc).name"
            
          />
          <q-toggle 
            class="text-caption" 
            dense size="xs"
            :true-value="false"
            :false-value="true"
            v-model="filterStore.selectFilters.holiday"
            toggle-indeterminate
            :label="filterStore.mainFilters.holiday.find(e => e.val == filterStore.selectFilters.holiday).name"
          >
            <q-tooltip>
              Учитывать только рабочие/выходные/все дни в выбранном периоде
            </q-tooltip>
        
        </q-toggle>
      </div>
      <div class="col-6 column self-end q-col-gutter-xs ">
       
          <q-toggle 
            class="text-caption" 
            dense size="xs"
         
            v-model="filterStore.percenterview"
           
            :label="percentlabel[filterStore.percenterview]"
          >
            <q-tooltip>
              Строить графики в процентах / значениях
            </q-tooltip>
        
        </q-toggle>
      </div>
    </div>
    </div>
      <div class="q-pl-xs self-end q-col-gutter-xs row ">
        <div class="col">
          <q-btn
            unelevated
            class="shadow-2"
          
            padding="sm"
            icon="mdi-text-search"
            :to="'statistic'"
          >
          <q-tooltip>Детализация</q-tooltip>
          </q-btn>
        </div>
        <div class="col">
          <q-btn
          unelevated
            class="shadow-2"
            padding="sm"
            icon="mdi-backspace-reverse"
            @click="filterStore.clear_filters()"
          >
          <q-tooltip>Сброс</q-tooltip>
          </q-btn>
        </div>

      
      </div>
    </div>
    
  </div>
</template>

<script>
import { ref, computed, watch } from "vue";

import UIFilter from "components/UI/UIFilter.vue";
import UIDateSelect from "components/UI/UIDateSelect.vue";
import { useFilterStore } from "stores/filter-store.js";

export default {
  components: {
    UIFilter,
    UIDateSelect,
    // MyHelper
  },

  setup() {
    const scalecjhanger=()=>{
     filterStore.selectFilters.mapscale=filterStore.mainFilters.mapscale.find(e=>e.id!=filterStore.selectFilters.mapscale.id)
    
    }
    // scalecjhanger
    const filterStore = useFilterStore();
    const percentlabel={true:"Проценты", false:"Значения"}
    const toogleEkc= ref(null)

    const mainSelectFilters = ref([
      // {
      //   title: "Масштаб карты",
      //   multi: false,
      //   storekey: "mapscale",
      //   col: "col-sm-4 col-lg-2 ",
      // },

      {
        title: "Территориальная единица",

        multi: true,
        storekey: "district",
        // 'regions'
        col: "col-sm-8 col-lg",
      },
      {
        title: "Статус",

        multi: false,
        storekey: "call_duration",
        col: "col-sm-4 col-lg-1",
      },
      {
        title: "Тип",

        multi: false,
        storekey: "call_type",
        col: "col-sm-4 col-lg-1",
      },
      {
        title: "Время",

        multi: false,
        storekey: "call_time_msc",
        col: "col-sm-4 col-lg-1",
      },
      {
        title: "Направление",

        multi: true,
        storekey: "direction",
        col: "col-sm-4 col-lg-2",
      },
    ]);

    const maindataSelectFilters = computed({
      get() {
        let res = mainSelectFilters.value;

        if (filterStore.selectFilters.mapscale.id == 1) {
          res[0].storekey = "district";
        } else {
          res[0].storekey = "regions";
        }

        return res;
      },
    });

    

    return {
      scalecjhanger,
      percentlabel,
      mainSelectFilters,
      filterStore,
      maindataSelectFilters,
      toogleEkc,
  
    };
  },
};
</script>

<style></style>
