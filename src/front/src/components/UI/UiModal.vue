<template>
  <q-card
    class="fit column "
    :style="`min-width: ${typeChar.size.w}px; max-height: ${typeChar.size.h}px`"
  >
  
  
    <div class="row q-pa-sm ">
      <div class="text-h6 q-px-xl">{{ typeChar.data.name }}</div>
     
      <q-space />
      <q-btn icon="close" flat round dense v-close-popup />
    </div>
    <q-separator />
    <div class="row column col ">
 
      <q-scroll-area
     
      class="fit "
    >     <div class="row justify-around">
      <div 
      :class="['ChartBar'].includes(typeChar.component)?'col-8':'col'"
      >
       <component  :is="typeChar.component"  :objData="typeChar.data" @directionfilter="directionfilter" />
      </div>
    </div>
        </q-scroll-area>
      
    </div>
    
  </q-card>
</template>

<script>
import ChartBar from "../dashboardpages/ChartBar.vue";
import ChartBarDistribution from "../dashboardpages/ChartBarDistribution.vue";
import ChartLine from "../dashboardpages/ChartLine.vue";
import ChartLineDynamics from "../dashboardpages/ChartLineDynamics.vue";

export default {
  components: {
    ChartBar,
    ChartLine,
    ChartLineDynamics,
    ChartBarDistribution
  },
  props: {
    typeChar: {
      type: Object,
      default: () => {
        return {};
      },
    },
  },
  setup(props,{emit}) {

    const directionfilter =(val)=>{
      emit('directionfilter',val)
    }


    return {directionfilter}
  }
};

</script>

<style scoped></style>
