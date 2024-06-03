<template>
  <div class="q-gutter-y-md">
    <SettingsInputDevices />

    <q-separator />

    <SettingsModel />

    <q-separator />

    <SettingsCollection title="Sampling">
    </SettingsCollection>
  </div>
</template>

<script setup lang="ts">
import SettingsCollection from './settings/SettingsCollection.vue';
import SettingsInputDevices from './settings/SettingsInputDevices.vue';
import SettingsModel from './settings/SettingsModel.vue';
</script>