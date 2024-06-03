<template>
  <SettingsCollection title="Input Devices">
    <div v-for="(mic, index) in settingsStore.devices" :key="index" class="row no-wrap justify-between">
      <q-toggle :label="settingsStore.micLabels[index]" v-model="mic.enabled" />
      <q-btn-group>
        <q-btn unelevated dense icon="arrow_upward" @click="settingsStore.moveDeviceUp(index)" />
        <q-btn unelevated dense icon="arrow_downward" @click="settingsStore.moveDeviceDown(index)" />
      </q-btn-group>
    </div>
  </SettingsCollection>
</template>

<script setup lang="ts">
/**
 * This component controls settings of input devices.
 */

import { useSettingsStore } from 'src/stores/settings-store';
import SettingsCollection from './SettingsCollection.vue';
const settingsStore = useSettingsStore();
</script>