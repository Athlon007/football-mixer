<template>
  <div class="row  flex-center">
    <div v-for="n in 17" :key="n" class="col text-center">
      <q-slider v-model="standard" :min="0" :max="50" color="slider-green" vertical reverse />
      <div class="q-pt-md">
        <q-badge outline class="text-h5 bg-primary">
          {{ standard }}
        </q-badge>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';


// Create dummy 17 sliders
const standard = ref(25);

</script>