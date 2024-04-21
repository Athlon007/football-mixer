<template>
  <q-page>
    <div class="full-width row justify-center q-pt-md">
      <football-field />
    </div>

    <div class="full-width">
      <sliders />
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Meta } from 'src/modules/models';
import FootballField from 'src/components/FootballField.vue';
import Sliders from 'src/components/Sliders.vue';


const meta = ref<Meta>({
  totalCount: 1200
});
</script>