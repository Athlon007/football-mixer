<template>
  <div>
  </div>
</template>

<script setup lang="ts">
import { useQuasar } from 'quasar';
import { useSystemStore } from 'src/stores/system-store';
import { onMounted } from 'vue';

const $q = useQuasar()
const systemStore = useSystemStore();

onMounted(async () => {
  checkStatus();
});

const checkStatus = async () => {
  try {
    await systemStore.check();
  } catch (error) {
    $q.notify({
      message: 'Back-end is not responding.',
      position: 'center',
      icon: 'warning',
      timeout: 0,
      color: 'negative',
      actions: [
        {
          label: 'Retry', color: 'white', handler: () => {
            checkStatus()
          }
        },
      ]
    });
  }
};

</script>