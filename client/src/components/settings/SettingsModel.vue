<template>
  <SettingsCollection title="Model">
    <q-select v-if="modelsStore.models" v-model="modelsStore.models.current_model" :options="modelsStore.models.models"
      option-label="name" option-value="name" emit-value map-options label="Model" @update:model-value="setModel"
      :loading="loadingModels">
      <template v-slot:prepend>
        <q-icon name="settings" />
      </template>
    </q-select>
    <q-skeleton v-else height="3em" />

    <div class="q-gutter-y-sm">
      <div>
        <div>
          <span class="text-bold">Version:</span> {{ currentModelDetails?.version }}
        </div>
        <div>
          <span class="text-bold">Recommended Sample Rate (ms):</span> {{
      currentModelDetails?.recommended_sampling_rate_ms }}
        </div>
      </div>
      <div class="text-italic" v-if="currentModelDetails?.recommended">
        This model is recommended for use with the current settings.
      </div>
    </div>
  </SettingsCollection>
</template>

<script setup lang="ts">
/**
 *  This component controls settings of ML model used.
 */

import SettingsCollection from './SettingsCollection.vue';
import { useModelStore } from 'src/stores/model-store';
import { computed, onMounted, ref } from 'vue';
import { useQuasar } from 'quasar';
import { useSystemStore } from 'src/stores/system-store';

const $q = useQuasar();
const modelsStore = useModelStore();
const loadingModels = ref(false);
const previousModel = ref<string>();
const systemStore = useSystemStore();

/**
 * Fetch models on component mount.
 */
onMounted(async () => {
  await checkStatus();
});

/**
 * Get details of the current model.
 */
const currentModelDetails = computed(() => {
  if (!modelsStore.models) {
    return null;
  }

  const currentName = modelsStore.models.current_model;
  return modelsStore.models.models.find((model) => model.name === currentName);
});

/**
 * Set the model to use.
 */
const setModel = async (model: string) => {
  loadingModels.value = true;

  try {
    await modelsStore.setModel(model);
  } catch (error) {
    console.error(error);
    // Restore previous model, if something goes wrong.
    if (modelsStore.models && previousModel.value) {
      modelsStore.models.current_model = previousModel.value;
    }

    $q.dialog({
      title: 'Error',
      message: 'Failed to set model. Please try again.',
      color: 'negative',
    });
  } finally {
    loadingModels.value = false;
  }
};

const checkStatus = async () => {
  try {
    await systemStore.check();
    await loadModels();
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

const loadModels = async () => {
  try {
    await modelsStore.getModels();
    // Store previous model, in case something goes wrong.
    previousModel.value = modelsStore.models?.current_model;
  } catch (error) {
    console.error(error);
  }
}

</script>

<style lang="scss" scoped></style>