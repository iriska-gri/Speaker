<template>
  <div >
    <div class="text-caption text-bold text-no-wrap">
      {{ title }}
    </div>

    <q-select
      dense
      outlined
      options-dense
      option-label="name"
      :multiple="multi"
      :use-input="multi"
      @filter="filterFn"
      v-model="selectFilter"
      :options="options"
      hide-hint
      emit-value
      class="ellipsis"
      
    >
    <template v-if="multi"
                v-slot:before-options>
                <q-item  clickable dense @click="takealldash">
                  <q-item-section side>
                    <q-checkbox
                      size="xs"
                      :model-value="selectFilter.length==options.length"
                      @update:model-value="takealldash"
                    />
              
                  </q-item-section>
                  <q-item-section>
                    <q-item-label
                      ><span  >Все
                      </span>
                     </q-item-label
                    >
                  </q-item-section>
                </q-item>
              </template>






      <template v-slot:option="{ itemProps, opt, selected }" v-if="multi">
        <q-item v-bind="itemProps">
          <q-item-section side>
            <q-checkbox
              size="xs"
              :model-value="selected"
              @update:model-value="
                filterStore.toggleOption(opt, storekey, multi)
              "
            />
          </q-item-section>
          <q-item-section>
            <q-item-label
              ><span v-if="'code'in opt && opt.code != '099o'">{{ opt.code }} - </span>
              {{ opt.name }}</q-item-label
            >
          </q-item-section>
        </q-item>
      </template>
      <template v-slot:selected v-if="multi">
        <div class="ellipsis">
          <q-chip
            dense
            v-for="x in selectFilter.slice(0, 2)"
            :key="x"
            class="no-margin"
          >
            {{ x.name.replace("федеральный округ", "") }}
          </q-chip>
          <q-tooltip>
            <div v-for="x in selectFilter" :key="x">
              {{ x.name }}
            </div>
          </q-tooltip>
        </div>
        <span
          class="text-caption"
          v-if="!!selectFilter && selectFilter.length > 2"
        >
          (+{{ selectFilter.length - 2 }})
        </span>

  
      </template>
    </q-select>
  </div>
</template>

<script>
import { ref, computed } from "vue";

import { useFilterStore } from "stores/filter-store.js";

export default {
  components: {},

  props: {
    title: {
      type: String,
      default: "Заголовок",
    },

    multi: {
      type: Boolean,
      default: false,
    },
    storekey: {
      type: String,
      default: "",
    },
  },

  setup(props, { emit }) {
    const filterStore = useFilterStore();
    const options = ref(filterStore.mainFilters[props.storekey]);
    const model = ref(null);

    const selectFilter = computed({
      get() {
        return filterStore.selectFilters[props.storekey];
      },
      set(newValue) {
        filterStore.selectFilters[props.storekey] = newValue;
      },
    });

    const filterFn = (val, update) => {
      if (val === "") {
        update(() => {
          options.value = filterStore.mainFilters[props.storekey];

          // here you have access to "ref" which
          // is the Vue reference of the QSelect
        });
        return;
      }

      update(() => {
        const needle = val.toLowerCase();
        options.value = filterStore.mainFilters[props.storekey].filter(
          (v) => `${v.code + v.name}`.toLowerCase().indexOf(needle) > -1
        );
      });
    };


    const takealldash=()=>{
      if (options.value.length==selectFilter.value.length){
        selectFilter.value=[]
      }
      else{
        options.value.forEach((e)=>{
            if(selectFilter.value.findIndex(m=>m.id==e.id)==-1){
              selectFilter.value.push(e)
            }
        })
      }

    }

    return {
      options,
      filterFn,
      model,
      filterStore,
      selectFilter,
      takealldash

      // options
    };
  },
};
</script>

<style>
.q-field__native {
  flex-flow: nowrap;
}
</style>
