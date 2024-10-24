<template>
  <Bar :data="data" :options="options" />
</template>

<script>
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";
import { Bar } from "vue-chartjs";

import ChartDataLabels from "chartjs-plugin-datalabels";
import { ref, computed } from "vue";
import { useFilterStore } from "stores/filter-store.js";
import { linear_tick_callback,linear_tick_callback_first_last } from '../../js/chartjs'
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ChartDataLabels
);

export default {
  name: "Distribution",
  components: {
    Bar,
  },

  props: {
    objData: {
      type: Object,
      default: () => {
        return {};
      },
    },
  },

  setup(props) {
    const filterStore = useFilterStore();

    const proc = (val, max) => {
      return val.map((e) => {
       
          let proc = Math.ceil((e * 100) / max);
       
          return proc;
        });
    }




    const data = computed({
      get() {        
        let datasets = JSON.parse(JSON.stringify(props.objData.datasets));
         if (filterStore.selectFilters.call_duration !== null && filterStore.selectFilters.call_duration.id == 1) {
          datasets[1].hidden = true;
          datasets[2].hidden = true;
        } else if ( filterStore.selectFilters.call_duration !== null && filterStore.selectFilters.call_duration.id == 2) {
          datasets[1].hidden = true;
          datasets[0].hidden = true;

        }
       else if ( filterStore.selectFilters.call_duration !== null && filterStore.selectFilters.call_duration.id == 3) {
          datasets[2].hidden = true;
          datasets[0].hidden = true;

        }
        return {labels: props.objData.labels, datasets: datasets};
      }
    }
    );
   

    const options = computed(
      {
        get() {
       let opts= {
      devicePixelRatio: 2,
      responsive: true,
      maintainAspectRatio: false,

      layout: {
        padding:{top: 5,  bottom:-3},
      },

      scales: {
        y: {
          display: props.objData.modal,
          ticks: {
            callback: (value, index, values) => { return linear_tick_callback(value, index, values, props.objData) }
          },
          beginAtZero: true,
          stacked: true,
          // max: filterStore.percenterview? 100:'',
          grid: {
            lineWidth: 1,

            // Пунктирная линия для оси X
          },
        },
        x: {
          display: props.objData.modal,
          stacked: true,
          ticks: {
    maxRotation: 0 // turns off rotation
  },
          grid: {
            lineWidth: 0,

            // Пунктирная линия для оси X
          },
        },
      },

      plugins: {
        tooltip: {
          enabled: true,
        },
        datalabels: {
          display: false,
         
          anchor: "center",
          align: "center",
          color: "rgb(245,255,250)",
          formatter: (value) => {
            if (value != 0) {       
              return value;
            }
          },

          font: {
            size: 11,
            family: "Onest-Golos",
          },
        },

        legend: {
          display: false,
        },
      },
    }
    if(filterStore.percenterview) opts.scales.y.max=100
    return opts
  }
})
  ;
    return {
      data,
      options,
    };
  },
};
</script>
