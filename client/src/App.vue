<template>
  <router-view />
</template>

<script setup lang="ts">
import { useQuasar } from 'quasar';
import { onBeforeMount } from 'vue';

const $q = useQuasar();

defineOptions({
  name: 'App'
});

onBeforeMount(() => {
  $q.dark.set(true);
});
</script>