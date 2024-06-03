<template>
  <q-layout view="lHh Lpr lFf">

    <q-drawer v-model="leftDrawerOpen" bordered :width="350">
      <q-list>
        <q-item-label header>
          Settings
        </q-item-label>

        <SettingsComponent />
      </q-list>
    </q-drawer>

    <q-page-container>
      <q-btn class="q-ml-md q-mt-md" outline size="2em" dense icon="settings" aria-label="Menu"
        @click="toggleLeftDrawer" />
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import SettingsComponent from 'src/components/SettingsComponent.vue';

defineOptions({
  name: 'MainLayout'
});

const leftDrawerOpen = ref(false);

const toggleLeftDrawer = () => {
  leftDrawerOpen.value = !leftDrawerOpen.value;
}
</script>

<style lang="scss" scoped>
.q-btn {
  // Makes drawer button not push the content
  position: absolute;
  z-index: 1;
}
</style>