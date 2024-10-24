<template>
  <q-page class="row">
    <div class="row column col-12">
      <div class="col-12">
        <q-img src="~assets/wolf.jpg" height="100%">
          <div class="absolute-full text-subtitle2 flex flex-center">
            Заглушка
          </div>
        </q-img>
      </div>
    </div>
  </q-page>
</template>

<script>
import { baseURL } from "src/boot/axios";
export default {
  setup() {
    return {
      baseURL,
    };
  },
};
</script>

<style></style>
