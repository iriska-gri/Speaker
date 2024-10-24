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
import { ref, computed, watch } from "vue";
import ChartDataLabels from "chartjs-plugin-datalabels";
import { useQuasar } from "quasar";
import { Screen } from "quasar";
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
  name: "App",
  components: {
    Bar,
  },

  props: {
    dataArr: {
      type: Object,
      default: () => {},
    },
  },

  setup(props) {
    const $q = useQuasar();
    function screensize() {
      if ($q.screen.xl) return 45;
      else if ($q.screen.lg) return 35;
      else if ($q.screen.md) return 35;
      else if ($q.screen.sm) return 35;
      else if ($q.screen.xs) return 10;
    }

    const data1 = () => {
      if (props.dataArr.type != "functionality") {
        return props.dataArr.x;
      }
      let max = Math.max(...props.dataArr.x);
      let arrNew = [];
      props.dataArr.x.forEach((e) => {
        arrNew.push(Math.ceil((e * 100) / max));
       
      });
     
      return arrNew;
    };

    const data2 = () => {
      let h = [];

      data1().forEach((e) => {
        h.push(100 - e);
      });

      return h;
    };

    const data = computed({
      get() {
        let datasets = [
          {
            label: "",
            backgroundColor: "rgba(30,136,229, 0.2)",
            borderColor: "rgb(30,136,229)",
            borderWidth: 1,
            data: data1(),
            barThickness: 20, 
   
          },

          {
            label: "",
            backgroundColor: ["rgba(245,245,245)"],
            borderColor: ["rgb(245,245,245)"],
            borderWidth: 1,
            data: data2(),
            barThickness: 20, 
        
          },
        ];
        if (props.dataArr.type == "tops") {
          datasets[0].backgroundColor = "rgba(140,204,143, 0.2)";
          datasets[0].borderColor = "rgba(102,187,106, 1)";
        }
        else if (props.dataArr.type == "tops_missed") {
          datasets[0].backgroundColor = "rgba(211,47,47, 0.2)";
          datasets[0].borderColor = "rgba(211,47,47, 0.5)";
        }

        
        return {
          labels: props.dataArr.y,
          datasets: datasets,
        };
      },
    });

    const options = {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: "y",

      layout: {
        padding: 10,
        boxHeight: 12
      },

      scales: {
        // xAxes: [{
        //     categoryPercentage: 1.0,
        //     barPercentage: 1.0
        // }],
        y: {
          beginAtZero: true,
          stacked: true,
         
          grid: {
            display: false,
          },
          ticks: {
            display: false,

            // display: false // Скрыть метки по оси Y
          },
        },
        x: {
          stacked: true,

          grid: {
            display: false,
          },
          ticks: {
            display: false,
          },
          barThickness: 10
        },
      },

      plugins: {
        tooltip: {
          enabled: false, // Отключаем подсказки
        },
        datalabels: {
          font: {
            size: 13,

            family: "Golos",
          },
          anchor: (value, index) => {
          
            if (value.datasetIndex == 0) {
              return "start";
            } else {
              return "end";
            }
          },

          align: (value, index) => {
            if (value.datasetIndex == 0) {
              return "right";
            } else {
              return "left";
            }
          },
          color: "rgb(0,0,0)",
          offset: 5,
          formatter: (value, index) => {
            if (index.datasetIndex == 0) {
              let text;
              index.chart.data.labels[index.dataIndex].length > screensize()
                ? (text =
                    index.chart.data.labels[index.dataIndex].slice(
                      0,
                      screensize()
                    ) + "...")
                : (text = index.chart.data.labels[index.dataIndex]);

              return text;
            } else {
              if (props.dataArr.type != "functionality") {
                return 100 - value + "%";
              } else {
             
                return props.dataArr.x[index.dataIndex];
              }
            }
          },
        },

        legend: {
          display: false,
        },
      },
    };
    return {
      data,
      options,
    };
  },
};
</script>
