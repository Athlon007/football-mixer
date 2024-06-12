<template>
  <SettingsCollection title="Experimental">
    <q-toggle v-model="settingsStore.useSmoothAudioFade" label="Use smooth audio fading" />
    <div class="bg-primary q-pa-sm rounded-md">
      <q-icon name="info" />
      Smooth audio fading is a feature that fades audio in and out smoothly to prevent binary transitions. The algorithm
      is unfinished and may not work as expected.
    </div>
  </SettingsCollection>
</template>

<script setup lang="ts">
import { useSettingsStore } from 'src/stores/settings-store';
import SettingsCollection from './settings/SettingsCollection.vue';

const settingsStore = useSettingsStore();
</script>

<style lang="scss" scoped></style>