<template>
 
  <LineJs :data="{ labels: objData.labels, datasets: objData.replay }" :options="options" />
</template>
  
<script lang="ts">

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  TimeScale,
  Filler
} from "chart.js";

import { Line as LineJs } from "vue-chartjs";
import { computed } from "vue";
import { linear_tick_callback,linear_tick_callback_first_last } from '../../js/chartjs'
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  TimeScale,
  Filler
);

export default {
  name: "App",
  components: {
    LineJs,
  },
  props: {
    objData: {
      type: Object,
      requiered: true,
      default: () => {
        return { replay: [], labels: [], modal: false };
      },
    },
  },

  setup(props) {


    const options = {
      devicePixelRatio: 2,
      responsive: true,
      maintainAspectRatio: false,
      layout: {
        padding: 10
      },
      scales: {
        x: {
          border: {
            dash: [5, 5]
          },
          grid: {
            lineWidth: 1,

            // Пунктирная линия для оси X
          },
          ticks: {
            maxRotation: 0,
            minRotation: 0,
            callback: (value, index, values) => { return linear_tick_callback_first_last(value, index, values, props.objData) }

          },
          display: props.objData.modal

        },
        y: {
          display: props.objData.modal,
          beginAtZero: true,
          ticks: {
            callback: (value, index, values) => { return linear_tick_callback(value, index, values, props.objData) }
          }
        }
      },
      plugins: {

        tooltip: {
          enabled: true

        },
        datalabels: {
          display: false,

          anchor: 'end',
          align: 'top',

          offset: 12,



        },

        legend: {
          display: props.objData.modal
        }
      }
    };
    return {
      // data,
      options,
    };
  },
};
</script>
  