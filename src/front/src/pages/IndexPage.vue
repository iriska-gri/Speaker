<template>
  <q-page class="flex flex-center">
    <img
      alt="Quasar logo"
      src="~assets/FNS-logo-header.png"
      style="width: 200px; height: 200px"
    >
  </q-page>
</template>

<script>
import { defineComponent } from 'vue'
import { boot } from 'quasar/wrappers'
export default defineComponent({
  name: 'IndexPage',
  setup(){
   window.location.href='/dash'
  }
})
</script>
