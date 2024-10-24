<template>
  <Bar
    :data="objData"
    :options="options"
    :style="` height: ${objData.labels.length * 45}px;`"
  />
  <!-- {{ objData.labels.length }} -->
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
import { computed, ref } from "vue";
import ChartDataLabels from "chartjs-plugin-datalabels";
import { useQuasar } from "quasar";
import { useFilterStore } from "stores/filter-store.js";
import { useRouter } from "vue-router";
import { createDOMCompilerError } from "@vue/compiler-dom";
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
    objData: {
      type: Object,
      default: () => {
        return { labels: [], datasets: [[]] };
      },
      requiered: true,
    },
   
  },

  setup(props, { emit }) {
    const filterStore = useFilterStore();
    const $q = useQuasar();
    const router = useRouter();
    function screensize() {
      if ($q.screen.xl) return 22;
      else if ($q.screen.xs) return 10;
      else return 35;
    }
    const scalefilter = (indexob) => {
      // console.log(props.objData.labelsfull[indexob[0].index].id);
      if (
        filterStore.selectFilters.mapscale.id == 1 &&
        filterStore.selectFilters.district.length == 0
      ) {
        let elm = filterStore.mainFilters.district.find(
          (el) => el.id == props.objData.labelsfull[indexob[0].index].id
        );
        filterStore.selectFilters.district = [elm];
      } else if (
        (filterStore.selectFilters.mapscale.id == 1 &&
          filterStore.selectFilters.district.length > 0) ||
        (filterStore.selectFilters.mapscale.id == 2 &&
          filterStore.selectFilters.regions.length == 0)
      ) {
        let elm = filterStore.mainFilters.regions.find(
          (el) => el.id == props.objData.labelsfull[indexob[0].index].id
        );

        filterStore.selectFilters.mapscale =
          filterStore.mainFilters.mapscale[1];
        filterStore.selectFilters.regions = [elm];
      } else {
        filterStore.addSelectFilters.level = filterStore.addictFilters.level[3];
        filterStore.tnofake = props.objData.labelsfull[indexob[0].index].id;
        // console.log(props.objData.labelsfull[indexob[0].index].id);
        router.push({ path: "/statistic" });
      }
    };

    
    const getmaxval = computed({
      get() {
        let max = Math.max(...props.objData.datasets[0].data);

        let indx = props.objData.datasets[0].data.indexOf(max);

        let maxsum = 0;

        props.objData.datasets.forEach((e) => {
          maxsum += e.data[indx];
        });

        if (props.objData.modal) maxsum += maxsum * 0.4;
        return maxsum;
      },
    });
    const colorizatortext = computed({
      get() {
        if (filterStore.percenterview)
          return props.objData.modal ? "white" : "#666666";
        return "#666666";
      },
    });
    const options = computed({
      get() {
        return {
          devicePixelRatio: 2,
          events: props.objData.clickable
            ? ["click", "mouseout", "mousemove"]
            : [],
          onHover: (e, chartElement) => {
            e.native.target.style.cursor = chartElement[0]
              ? "pointer"
              : "default";
          },

          onClick: (e, indexob) => {
            if (props.objData.clickable) {
              if (props.objData.clickfunction == "scalefilter") {
                scalefilter(indexob);
              } else if (props.objData.clickfunction == "directionfilter") {
                // console.log(props.objData);
                emit(
                  "directionfilter",
                  props.objData.labelsfull[indexob[0].index].id
                );
              }
            }
          },
          datasets: {
            bar: { barPercentage: 0.1 },
          },
          responsive: true,
          maintainAspectRatio: false,
          indexAxis: "y",

          layout: {
            padding: props.objData.modal
              ? {}
              : { top: 5, left: -50, bottom: -10 },
          },
          // top: 5, left:200, right:200, bottom:-10

          scales: {
            y: {
              beginAtZero: true,
              stacked: true,

              grid: {
                display: false,
              },
              ticks: {
                display: props.objData.modal ? true : false,
                // crossAlign:'center'
                // mirror: true,
                padding: 10,
                font: {
                  size: 13,
                  weight: "bold",
                  family: "Golos",
                },
              },
            },
            x: {
              stacked: true,
              max: filterStore.percenterview ? 100 : getmaxval.value,
              grid: {
                display: false,
              },
              ticks: {
                display: false,
              },
              // barThickness: 20,
            },
          },

          plugins: {
            ChartDataLabels,
            tooltip: {
              enabled: false, // Отключаем подсказки
            },
            datalabels: {
              color: colorizatortext.value,

              font: {
                size: 13,
                weight: "",
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
                  return props.objData.modal ? 0 : -45;
                } else {
                  return props.objData.modal
                    ? filterStore.percenterview
                      ? 180
                      : 0
                    : 240;
                }
              },
              padding: (value, index) => {
                if (value.datasetIndex != 0) {
                  return {
                    bottom: props.objData.modal ? 0 : 5,
                    right: props.objData.modal ? 0 : 75,
                  };
                }
              },
              offset: 8,

              formatter: (value, index) => {
                
                // console.log(index.chart.data.labels[index.dataIndex].length, screensize(), 'index.chart.data.labels[index.dataIndex]')
                if (index.chart.data.labels[index.dataIndex] === undefined)
                  return "";
                let text =
                  index.chart.data.labels[index.dataIndex].length > screensize()
                    ? index.chart.data.labels[index.dataIndex].slice(
                        0,
                        screensize()
                      ) + "..."
                    : index.chart.data.labels[index.dataIndex] + " ";

                if (index.datasetIndex == 0) {
                  if (filterStore.percenterview) {
                    return props.objData.modal
                      ? `${value}% (${props.objData.factdata[
                          [index.dataIndex]
                        ][0].toLocaleString("ru-RU")})`
                      : text;
                  } else {
                    return props.objData.modal ? `` : text;
                    // return props.objData.modal ? `${value.toLocaleString("ru-RU")} (${props.objData.factdata[[index.dataIndex]][0].toFixed(2)}%)` : text;
                  }
                } else if (
                  index.datasetIndex ==
                  props.objData.datasets.length - 1
                ) {
                  if (filterStore.percenterview) {
                    return props.objData.modal
                      ? `${value}% (${props.objData.factdata[
                          [index.dataIndex]
                        ][1].toLocaleString("ru-RU")})`
                      : `${
                          props.objData.datasets[0].data[index.dataIndex]
                        }% (${props.objData.factdata[
                          [index.dataIndex]
                        ][0].toLocaleString("ru-RU")})`;
                  } else {
                    return `${props.objData.datasets[0].data[
                      index.dataIndex
                    ].toLocaleString("ru-RU")} (${props.objData.factdata[
                      [index.dataIndex]
                    ][0].toFixed(2)}%)`;
                    // return props.objData.modal ? `${value.toLocaleString("ru-RU")} (${props.objData.factdata[[index.dataIndex]][1].toFixed(2)}%)` :
                    // `${props.objData.datasets[0].data[index.dataIndex].toLocaleString("ru-RU")} (${props.objData.factdata[[index.dataIndex]][0].toFixed(2)}%)`;
                  }
                } else {
                  return "";
                }
              },
            },

            legend: {
              display: false,
            },
          },
        };
      },
    });
    return {
      // data,
      options,
    };
  },
};
</script>
