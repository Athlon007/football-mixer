<template>
  <div class="q-gutter-y-md">
    <SettingsCollection title="Input Devices">
      <div v-for="(mic, index) in settingsStore.devices" :key="index" class="row no-wrap justify-between">
        <q-toggle :label="mic.device.label" v-model="mic.enabled" />
        <q-btn-group>
          <q-btn unelevated dense icon="arrow_upward" @click="settingsStore.moveDeviceUp(index)" />
          <q-btn unelevated dense icon="arrow_downward" @click="settingsStore.moveDeviceDown(index)" />
        </q-btn-group>
      </div>
    </SettingsCollection>

    <q-separator />

    <SettingsCollection title="Model">
    </SettingsCollection>

    <q-separator />

    <SettingsCollection title="Sampling">
    </SettingsCollection>
  </div>
</template>

<script setup lang="ts">
import { useSettingsStore } from 'src/stores/settings-store';
import SettingsCollection from './settings/SettingsCollection.vue';

const settingsStore = useSettingsStore();
</script>