<template>
  <SettingsCollection title="Sampling">
    <q-input v-model="settingsStore.sampleRate" label="Sample Rate (ms)" type="number" :rules="rules">
      <template v-slot:prepend>
        <q-icon name="timer" />
      </template>
    </q-input>
  </SettingsCollection>
</template>

<script setup lang="ts">
import { useSettingsStore } from 'src/stores/settings-store';
import SettingsCollection from './SettingsCollection.vue';

const settingsStore = useSettingsStore();

/** Validation rules for sample rate.*/
const rules = [
  (v: string) => !!v || 'Required',
  (v: string) => !isNaN(Number(v)) || 'Must be a number',
  (v: string) => Number(v) > 10 || 'Must be greater than 10',
  (v: string) => Number(v) < 10000 || 'Must be less than 10000',
];
</script>

<style lang="scss" scoped></style>