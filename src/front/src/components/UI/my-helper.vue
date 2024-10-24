<template>
  <div class="pa-0 align-self-center">
    <!-- <div
      class="inline bg-amber rounded-borders cursor-pointer"
      style="max-width: 300px"
    > -->
   
    <q-btn round color="primary" icon="shopping_cart" />
      <!-- <div class="flex flex-center text-center non-selectable q-pa-md">
       no-pointer-events
      </div> -->

      <q-menu touch-position>
        <pre
          >{{ pretext }}
</pre
        >
      </q-menu>
   
  </div>
</template>

<script>
import { ref } from "vue";

export default {
  name: "myHelper",

  props: {
    pretext: {
      type: Object,
      default: () => {},
    },
  },

  setup() {
    const menu = ref(false);

    return { menu };
  },

  // d
};
</script>

<style>
.whmy {
  height: 950px !important;
}
</style>


      <!-- <svg
                  ref="maprus"
                  class="cursor-pointer q-pa-lg"
                  @click="click_mouse"
                  @mousemove="over_mouse"
                  @mousedown.prevent="downMouse"
                  @mouseup.prevent="upMouse"
                  @mouseleave.prevent="clickMouse = false"
                  @mouseout="hideTooltip"
                  @wheel.prevent="mouseWheel"
                  @contextmenu.prevent="openModal"
                  xmlns:svg="http://www.w3.org/2000/svg"
                  xmlns="http://www.w3.org/2000/svg"
                  xmlns:xlink="http://www.w3.org/1999/xlink"
                  version="1.2"
                  baseProfile="tiny"
                  x="0px"
                  y="0px"
                  :viewBox="viewBox"
                  xml:space="preserve"
                  xmlns:xml="http://www.w3.org/XML/1998/namespace"
                > -->