<template>
  <LineJs :data="objData" :options="options" />
</template>

<script>
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
  Filler,
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
  name: "Linef",
  components: {
    LineJs,
  },

  props: {
    objData: {
      type: Object,
      required: true,
      default: () => {
        return {labels:[], datasets:[]};
      },
    },
    // modal: {
    //   type: Boolean,
    //   default: false,
    // },
  },

  setup(props) {
  

    const superopt = {
      recall: {
        scalesy: {
          suggestedMin: 100,
          suggestedMax: 100,
        },
        text: {
          y: "%",
        },
        datasets: {
          fill: true,
        },
      },

      dynamiccall: {
        scalesy: {},
        text: {
          y: "с",
        },
        datasets: {},
      },
    }

    const options = computed({
      get() {
        let yscales = {}
        if(!props.objData.modal){
          yscales.y={display:false}
          console.log("NOMOD");
        }else{
          console.log("modal");
          yscales.y={
            display: true,
            position:"left",
          beginAtZero: true,
          ticks: {
            callback: function (value, index, values) {            
              
              // if (props.objData.modal != true) {
              // {
              //   let half = Math.ceil(values.length / 4);
              //   let halfOne = half + half;
              //   if (
              //     index === 0 ||
              //     index === half ||
              //     index === halfOne ||
              //     index === values.length - 1
              //   ) {
                  return value + superopt[props.objData.type].text.y;
                // }
                // return "";
              } 
            }}}
        
        

        for (let key of Object.keys(superopt[props.objData.type].scalesy)) {
          yscales.y[key] = superopt[props.objData.type].scalesy[key];
        }
        if (props.objData.type=='recall' ){
            if(
              props.objData.modal!=true
            ){
              yscales.y1= {display: false}
            }else{
          yscales.y1= {

            type: 'linear',
            display: true,
            position: 'right',

            // grid line settings
            grid: {
              drawOnChartArea: false, // only want the grid lines for one axis to show up
            },
          }
      }
        }

        return {
          devicePixelRatio: 2,
          responsive: true,
          maintainAspectRatio: false,
          layout: {
            padding:{top: 5,  bottom:-3},
          },
          scales: { 
            
            x: {
              display: false,
              border: {
                dash: [5, 5],
              },

              grid: {
                lineWidth: 1,

                // Пунктирная линия для оси X
              },
              ticks: {
                maxRotation: 0,
                minRotation: 0,
                callback: function (value, index, values) { return linear_tick_callback_first_last(value, index, values,props.objData)
                 
                },
              },
            },
          ...yscales,
            
          },
          plugins: {
            tooltip: {
            enabled: true,
    },
            datalabels: {
              display: false,
                   
            },
            legend: {
              display: false,
            },
          },
        };
      },
    });

  

    // options.scales.y = superopt[props.objData.type].scalesy;

    return {
     
      options,
    };
  },
};
</script>
