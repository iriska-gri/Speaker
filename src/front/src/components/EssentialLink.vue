<template>
  <div class="q-pa-xs" style="max-width: 250px">
    <q-list class="text-grey-7">
      <!-- <q-separator spaced /> -->

      <q-item
        class="rounded-borders"
        clickable
        v-ripple
        active-class="background"
        dense
        :to="link"
        
      >
        <q-item-section avatar>
          <q-icon :name="ico"  size="sm" />
        </q-item-section>

        <q-item-section>{{ title }} </q-item-section>
      </q-item>
    </q-list>
  </div>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
  name: "EssentialLink",
  props: {
    title: {
      type: String,
      required: true,
    },

    link: {
      type: String,
      default: "#",
    },

    ico: {
      type: String,
      default: "",
    },
  },

  setup(props) {
    return {};
  },
});
</script>

<style>
.background {
  background: rgba(30, 136, 229, 0.2);
  color: rgba(21,101,192); 
}
</style>
