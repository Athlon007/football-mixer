<template>
  <div class="q-gutter-y-md">
    <SettingsInputDevices />

    <q-separator />

    <SettingsModel />

    <q-separator />

    <SettingsSamples />
  </div>
</template>

<script setup lang="ts">
import SettingsInputDevices from './settings/SettingsInputDevices.vue';
import SettingsModel from './settings/SettingsModel.vue';
import SettingsSamples from './settings/SettingsSamples.vue';
</script>