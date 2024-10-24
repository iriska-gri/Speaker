<template>
  <q-layout view="hHh lpR fFf">
    <q-header bordered :class="$q.dark.isActive ? 'bg-dark ' : 'bg-white text-black'">
      <q-toolbar class="q-pl-md q-pr-none row">
        <q-btn class="q-my-sm" round @click="toggleLeftDrawer">
          <q-avatar size="42px">
            <img src="~assets/FNS-logo-header.png" />
          </q-avatar>
        </q-btn>
        <div
          class="col-1 q-px-sm q-pt-sm no-pointer-events text-mycolor text-uppercase text-caption text-weight-bold text_gam">
          <div>Федеральная</div>
          <div>налоговая служба</div>
        </div>

        <q-separator vertical inset black />
        <div class="col q-ml-md row items-center">
          <q-avatar size="42px ">
            <img v-if="$q.dark.isActive" src="~assets/dynamik.png" />
            <img v-else src="~assets/dynamic_black.png" />
          </q-avatar>

          <q-toolbar-title class="no-pointer-events text-h6">
            {{ productName }}
          </q-toolbar-title>
        </div>

        <div class="column ">
          <div class="no-pointer-events text-caption self-end">{{ version }}</div>
          <!-- <q-separator inset black /> -->
          <div class="row ">
            
            <div class="skewx-45deg self-end cursor-pointer" @click="showing=!showing ">
              
              <div>
              <q-icon name="mdi-filter-outline " size="md" color="grey-8"></q-icon>
              <q-icon name="mdi-arrow-up-down" size="" color="grey-8"></q-icon>
              </div>
            
            </div>
            <!-- <div>
                        <q-btn-dropdown flat icon="mdi-filter-outline">

                          <div class="row">
                            <FilteredComp class="col bg-red" />

                          </div>

                        </q-btn-dropdown>

            </div> -->

            <div class="column">
              <q-btn size="13px" round flat @click="toggleTheme" :icon="$q.dark.isActive ? 'mdi-weather-sunny' : 'mdi-weather-night'
                " />
            </div>
            <div class="column flex self-end bg-red">
              <q-menu
              persistent
              style='width:100%'
              anchor="bottom end" 
              
              v-model="showing"
        >
        <div class="row">
         
          <FilteredComp class="col q-pa-sm" />
        </div>
      </q-menu>
            </div>
          </div>
        </div>
      </q-toolbar>
    </q-header>

    <q-drawer overlay :width="200" v-model="leftDrawerOpen" bordered>
      <q-list>
        <EssentialLink v-for="link in essentialLinks" :key="link.title" v-bind="link" />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { version, productName } from "../../package.json";
import { defineComponent, ref, computed } from "vue";
import { useQuasar } from "quasar";
import FilteredComp from "../components/dashboardpages/FilteredComp.vue";
import EssentialLink from "components/EssentialLink.vue";

const linksList = [
  {
    title: "Дашборд",
    link: "dash",
    ico: "mdi-chart-areaspline",
  },
  {
    title: "Статистика",
    link: "statistic",
    ico: "mdi-table",
  },
  {
    title: "Песочница",
    link: "sunBox",
    ico: "mdi-table",
  },
];

export default defineComponent({
  name: "MainLayout",

  components: {
    EssentialLink,
    FilteredComp,
  },

  setup() {
    const $q = useQuasar();
    const leftDrawerOpen = ref(false);

    const menuwidth=computed({get(){
      return `width:`
    }})


    const toggleTheme = () => {
      $q.dark.toggle();
      localStorage.setItem("dozvon-settings", JSON.stringify({ darkmode: $q.dark.isActive }))
    };


    if (localStorage.getItem("dozvon-settings") !== null) {
      let settings = JSON.parse(localStorage.getItem("dozvon-settings"))
      $q.dark.set(settings.darkmode)
    } else {
      localStorage.setItem("dozvon-settings", JSON.stringify({ darkmode: $q.dark.isActive }))
    }

    return {
      showing: ref(false),
      toggleTheme,
      version,
      productName,
      essentialLinks: linksList,
      leftDrawerOpen,
      toggleLeftDrawer() {
        leftDrawerOpen.value = !leftDrawerOpen.value;
      },
    };
  },
});
</script>
<style>
.text_gam {
  font-size: 0.6rem;
  line-height: 0.8rem;
}
.skewx-45deg {
  width: 84px;
  height: 0px;
  border-bottom: 35px solid white;
  border-right: 0 solid transparent;
  border-left: 35px solid transparent;
}

</style>
