<template>
  <q-page class="row q-col-gutter-y-xs bg-green">
    <div class="col column">
      <div class="col-10 col-lg-10 col-sm-7 row">
        
        <div class="col-lg-8 col-md-12 col-sm-12 bg-green">1</div>
        <div class="col-lg-4 col-md-12 col-sm-12 row bg-yellow">
            
          <div class="bg-yellow col-lg-6 col-md-6 col-sm-6">2</div>
          <div class="bg-blue col-lg-6 col-md-6 col-sm-6">3</div>
        </div>
      </div>
      <div class="col-2 col-lg-2 col-sm-5 row">
        <div v-for="x in 4" :key="x" class="col-lg-3 col-sm-6" :class="`bg-red`">
          {{ x }}
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
export default {
  setup() {
    return {};
  },
};
</script>

<style></style>
