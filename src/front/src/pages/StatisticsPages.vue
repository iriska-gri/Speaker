<template>
  <q-page class="column q-col-gutter-y-xs">
    <div class="col-2 column q-px-sm q-col-gutter-y-xs">
      <div class="row q-col-gutter-xs">

        <div v-for="(x, index) in maindataSelectFilters" :key="x" :class="x.col">
          <div>
            <div class="text-caption text-bold text-no-wrap">
              {{ x.title }}
            </div>

            <q-select dense outlined options-dense option-label="name" :multiple="x.multi" :use-input="x.multi"
              v-model="filterStore[x.modelstore][x.storekey]" :options="x.store" hide-hint
              @filter="(inputValue, doneFn) => filterFn(inputValue, doneFn, index)" emit-value :rows-per-page="0"
              class="cursor-pointer">
              <template v-slot:before-options>
                <q-item @click="takeall(x)" clickable dense v-if="x.multi">
                  <q-item-section side>
                    <q-checkbox size="xs" :model-value="x.store.length == filterStore[x.modelstore][x.storekey].length"
                      @update:model-value="takeall(x)" />

                  </q-item-section>
                  <q-item-section>
                    <q-item-label><span>Все
                      </span>
                    </q-item-label>
                  </q-item-section>
                </q-item>
              </template>
              <template v-slot:option="{ itemProps, opt, selected }" v-if="x.multi">
                <q-item v-bind="itemProps">
                  <q-item-section side>
                    <q-checkbox size="xs" :model-value="selected" @update:model-value="x.modelstore != 'addSelectFilters' ?
                      filterStore.toggleOption(opt, x.storekey, x.multi) :
                      filterStore.toggleaddOption(opt, x.storekey, x.multi)
                      " />
                  </q-item-section>
                  <q-item-section>
                    <q-item-label><span v-if="'code' in opt && opt.code != '099o'">{{ opt.code }}
                      </span>
                      {{ opt.name }}</q-item-label>
                  </q-item-section>
                </q-item>
              </template>
              <template v-slot:selected v-if="x.multi">
                <div class="ellipsis">
                  <q-chip dense v-for="y in filterStore[x.modelstore][x.storekey].slice(
                    0,
                    3
                  )" :key="y" class="no-margin cursor-pointer">

                    <div>
                      {{
                        y.code == null
                        ? (y.code = "Иное")
                        : y.code.replace("099o", "НТ")
                      }}
                    </div>

                    <q-tooltip>
                      {{ y.name }}
                    </q-tooltip>
                  </q-chip>
                </div>

                <span>
                  <span class="text-caption q-pl-xs cursor-pointer" v-if="!!filterStore[x.modelstore][x.storekey] &&
                    filterStore[x.modelstore][x.storekey].length > 3
                    ">
                    (+{{ filterStore[x.modelstore][x.storekey].length - 3 }})
                    <q-tooltip>
                      <div v-for="y in filterStore[x.modelstore][x.storekey]" :key="y">
                        {{ y.name }}
                      </div>
                    </q-tooltip>
                  </span>
                </span>
              </template>
            </q-select>
          </div>
        </div>

        <div v-for="x in inputs" :key="x" :class="x.col">
          <div>
            <div class="text-caption text-bold text-no-wrap">{{ x.title }}</div>
            <q-input dense outlined v-model="filterStore[x.modelstore][x.storekey]"></q-input>
          </div>
        </div>
        <div v-for="x in lastfilters" :key="x" :class="x.col">
          <div class="text-caption text-bold text-no-wrap">{{ x.title }}</div>

          <q-select dense outlined options-dense :option-label="x.name" :multiple="x.multi" :use-input="x.multi"
            v-model="filterStore[x.modelstore][x.storekey]" :options="x.store" hide-hint emit-value>
           
            <template v-if="x.multi" v-slot:before-options>
              <q-item clickable dense>
                <q-item-section side>
                  <q-checkbox size="xs" :model-value="x.store.length == filterStore[x.modelstore][x.storekey].length"
                  
                    />

                </q-item-section>
                <q-item-section  @click="takeall(x)" >
                  <q-item-label><span>Все 
                  
                    </span>
                  </q-item-label>
                </q-item-section>
              </q-item>
            </template>

            <template v-slot:option="{ itemProps, opt, selected, toggleOption  }" v-if="x.multi">
              <q-item v-bind="itemProps">
                <q-item-section side>
                  <q-checkbox size="xs" :model-value="selected" @update:model-value="toggleOption(opt) " />
                </q-item-section>
                <q-item-section>
                  <q-item-label> {{ opt[x.name] }}</q-item-label>
                </q-item-section>
              </q-item>
            </template>
            <template v-slot:selected v-if="x.multi">
              <div class="no-wrap ellipsis">
                <q-chip dense v-for="y in filterStore[x.modelstore][x.storekey].slice(0, 3)" :key="y"
                  class="no-margin cursor-pointer">
                  {{ y[x.shortname] }}


                  <q-tooltip>
                    <div v-for="y in filterStore[x.modelstore][x.storekey]" :key="y">

                      {{ y[x.name] }}
                    </div>
                  </q-tooltip>
                </q-chip>

              </div>
            </template>
            <template v-slot:append v-if="x.multi">
              <span class="text-caption q-pl-xs cursor-pointer" v-if="!!filterStore[x.modelstore][x.storekey] &&
                filterStore[x.modelstore][x.storekey].length > 2
                ">
                (+{{ filterStore[x.modelstore][x.storekey].length - 2 }})
              </span>
            </template>
          </q-select>
        </div>

        <div class="col-sm-4 col-lg-2 row q-col-gutter-xs">
          <div class="col" v-for="(x, index) in ['Период']" :key="x">
            <UIDateSelect :title="x" :index="index" />
          </div>
        </div>

        <div class="col column self-end q-col-gutter-xs">
          <q-toggle class="text-caption" dense size="xs" v-model="filterStore.selectFilters.from_ekc" toggle-indeterminate :label="filterStore.mainFilters.from_ekc.find(e => e.val == filterStore.selectFilters.from_ekc).name" />
          <q-toggle class="text-caption" dense size="xs" v-model="filterStore.selectFilters.holiday" :true-value="false"
            :false-value="true" toggle-indeterminate
            :label="filterStore.mainFilters.holiday.find(e => e.val == filterStore.selectFilters.holiday).name">
            <q-tooltip>
              Учитывать только рабочие/выходные/все дни в выбранном периоде
            </q-tooltip>

          </q-toggle>
        </div>
        <div class="self-end justify-end q-col-gutter-sm row ">
          <div class="col-5">
            <q-btn color="blue-9" class="text-subtitle2 ellipsis full-width text-capitalize" label="Применить"
              size="1.1em" @click="startsearch" :disable="loading" />
          </div>
          <!-- :disable="changingFilter()" -->
          <div class="col-5">
            <q-btn color="grey-4" class="text-black text-subtitle2 ellipsis full-width text-capitalize" label="Сбросить"
              size="1.1em" @click="filterStore.clear_all_filters()" />
          </div>
        </div>
      </div>
    </div>
    <div class="col row">
      <StatisticTable @getsubinfo="startsearch" :tabledata="tabledata.data" :avgrussia="tabledata.avgrussia"
        :addcolumns="addcolumns" :loading="loading" />
    </div>
  </q-page>
</template>

<script>
import { api } from "boot/axios";
import { ref, computed, watch } from "vue";
import StatisticTable from "components/statistic/StatisticTable.vue";
import UIDateSelect from "components/UI/UIDateSelect.vue";
import { useFilterStore } from "stores/filter-store.js";
export default {
  components: {

    UIDateSelect,
    StatisticTable,

  },
  setup() {

    const tabledata = ref([]);
    const loading = ref(false)
    const filterStore = useFilterStore();
    filterStore.getaddfilters(filterStore.addictFilters);
    filterStore.avgmapView = false




    const setindicator = () => {

      [
        filterStore.selectFilters.call_duration,
        filterStore.selectFilters.call_time_msc,
      ].forEach((e) => {
        let ind = filterStore.addictFilters.indicator.findIndex(
          (m) => m.field === e.field
        );

        if (
          ind > -1 &&
          filterStore.addSelectFilters.indicator.findIndex(
            (n) => n.field == e.field
          ) == -1
        ) {
          filterStore.addSelectFilters.indicator.push(filterStore.addictFilters.indicator[ind]);
          if (['accepted', 'missed', 'dropped'].includes(filterStore.addictFilters.indicator[ind].field)) {
            filterStore.addSelectFilters.indicator.push(filterStore.addictFilters.indicator.find(el => el.field == `${filterStore.addictFilters.indicator[ind].field}_p`))
          }
        }
      });
      if (filterStore.addSelectFilters.indicator.length == 0) {
        filterStore.addictFilters.indicator.forEach((e, index) => { if (e.defaultshow == true) filterStore.addSelectFilters.indicator.push(e) })
      }
    };
    setindicator();
    const mainSelectFilters = computed({
      get() {
        return [
          {
            title: "Федеральные округа",

            multi: true,
            modelstore: "selectFilters",
            store: filterStore.mainFilters.district
       
            ,
            storekey: "district",
            onScroll: null,
            col: "col-sm-4 col-lg-2",
          },

          {
            title: "Регионы",
            onScroll: null,
            multi: true,
            modelstore: "selectFilters",
            store: filterStore.mainFilters.regions,

            storekey: "regions",
            col: "col-sm-8 col-lg-2",
          },

          {
            title: "Инспекции",
            modelstore: "addSelectFilters",
            store: filterStore.addictFilters.tno,

            multi: true,
            storekey: "tno",
            col: "col-sm-4 col-lg-2",
          },
          
       
        ]}});
    const inputs = ref([
      {
        title: "Отделы",
        modelstore: "addSelectFilters",

        storekey: "department",
        col: "col-sm-4 col-lg-2",
      },
      {
        title: "Сотрудники",
        modelstore: "addSelectFilters",
        storekey: "person",
        col: "col-sm-4 col-lg-2",
      },

    ]
  );

  const maindataSelectFilters = computed({
    get() {
      let res = mainSelectFilters.value;
      return res;
    },
  });

  const lastfilters = ref([
  {
            title: "Тип вызова",  
            name: "name",         
            modelstore: "selectFilters",
            store: computed(()=> {return filterStore.mainFilters.call_type}),      
            storekey: "call_type",
            col: "col-sm-8 col-lg-2",



          },
          // {title: "Время",  
          //   name: "name",         
          //   modelstore: "selectFilters",
          //   store: filterStore.mainFilters.call_time_msc,
          //   storekey: "call_time_msc",
          //   col: "col-sm-8 col-lg-2",



          // },

          
    {
      title: "Показатели",
      name: "label",
      shortname: "shortlabel",
      modelstore: "addSelectFilters",
      store: filterStore.addictFilters.indicator,
      
      multi: true,
      storekey: "indicator",
      col: "col-sm-4 col-lg-4",
    },
    {
      title: "Уровень отображения",
      name: "name",
      modelstore: "addSelectFilters",
      store: computed(()=> {return filterStore.addictFilters.level; }),
      multi: false,
      storekey: "level",
      col: "col-sm-4 col-lg-2",
    },
    
  ]);
  const addcolumns = ref([]);
  const apicontroller = ref(new AbortController());
  const startsearch = ({ sublevel = 0, row = {} } = {}) => {
    if (loading.value == true) {
      apicontroller.value.abort()
    
      apicontroller.value = new AbortController();
    }
    loading.value = true
    let filter = filterStore.mainfiltersdetalize(sublevel, row);

    api.post("/atc/getlevelinfo/", filter, { signal: apicontroller.value.signal, }).then((res) => {

      // totalows.value=res.data.totalows
      tabledata.value = res.data;
      loading.value = false
      addcolumns.value = filterStore.addSelectFilters.indicator;
    }



    );

  };

  if(filterStore.selectFilters.period.from.length > 0) {
  startsearch();
}
watch(
  () => filterStore.selectFilters.period,
  (newValue, oldValue) => {
    // console.log(filterStore.selectFilters.period);
    if (oldValue.from.length == 0) {
      startsearch();
    }
  },
  { deep: true, once: true }
);


watch(
  () => filterStore.selectFilters.district,
  (newValue, oldValue) => {
    if (
      newValue.length > 0 &&
      filterStore.selectFilters.regions.length > 0
    ) {
      filterStore.selectFilters.regions =
        filterStore.selectFilters.regions.filter((e) =>
          newValue
            .reduce((arr, elm) => [...arr, elm.id], [])
            .includes(e.parent)
        );
    }
    if (
      filterStore.addSelectFilters.tno.length > 0 &&
      newValue.length > 0
    ) {
      filterStore.addSelectFilters.tno =
        filterStore.addSelectFilters.tno.filter((e) =>
          newValue
            .reduce((arr, elm) => [...arr, elm.id], [])
            .includes(e.parent__parent)
        );
    }
  },
  { deep: true }
);

watch(
  () => filterStore.selectFilters.regions,
  (newValue, oldValue) => {
    if (
      newValue.length > 0 &&
      filterStore.addSelectFilters.tno.length > 0
    ) {
      filterStore.addSelectFilters.tno =
        filterStore.addSelectFilters.tno.filter((e) =>
          newValue
            .reduce((arr, elm) => [...arr, elm.id], [])
            .includes(e.parent)
        );
    }
  },
  { deep: true }
);

const filterFn = (val, update, index) => {

  if (val === "") {
    update(() => {
      if (index == 0) {
        mainSelectFilters.value[index].store = filterStore.mainFilters[mainSelectFilters.value[index].storekey]
      }
      else if (index == 1) {
        if (filterStore.selectFilters.district.length > 0) {
          mainSelectFilters.value[index].store = filterStore.mainFilters.regions.filter((e) =>
            filterStore.selectFilters.district
              .reduce((arr, el) => [...arr, el.id], [])
              .includes(e.parent)
          );

        } else { mainSelectFilters.value[index].store = filterStore.mainFilters[mainSelectFilters.value[index].storekey] }
      }
      else if (index == 2) {
        let res = filterStore.addictFilters.tno;
        if (filterStore.selectFilters.district.length > 0) {
          res = res.filter((e) =>
            filterStore.selectFilters.district
              .reduce((arr, el) => [...arr, el.id], [])
              .includes(e.parent__parent)
          );
        }
        if (filterStore.selectFilters.regions.length > 0) {
          res = res.filter((e) =>
            filterStore.selectFilters.regions
              .reduce((arr, el) => [...arr, el.id], [])
              .includes(e.parent)
          );
        }
        mainSelectFilters.value[index].store = res;

      }
    });
    return;
  }

  update(() => {
    const needle = val.toLowerCase();
    mainSelectFilters.value[index].store = maindataSelectFilters.value[index].store.filter(
      (v) => `${v.code + v.name}`.toLowerCase().indexOf(needle) > -1
    );
  });
};
const takeall = (x) => {

  if (x.store.length == filterStore[x.modelstore][x.storekey].length) {
    filterStore[x.modelstore][x.storekey] = []
  }
  else {
   
    x.store.forEach((e) => {
      if (filterStore[x.modelstore][x.storekey].findIndex(el => e.id == el.id) == -1) {
        filterStore[x.modelstore][x.storekey].push(e)
      }
    }
    )
  }

}


return {
  // totalows,
  takeall,
  filterFn,
  mainSelectFilters,
  startsearch,
  tabledata,
  inputs,
  lastfilters,
  addcolumns,
  filterStore,
  maindataSelectFilters,
  loading,
  toogleEkc: ref(null)
};
  },
};
</script>

<style>
.my-fylter .q-field__native {
  flex-flow: nowrap;
}
</style>
