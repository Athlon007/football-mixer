<template>
  <div class="q-px-md">
    <q-item-label v-if="title" class="text-bold text-h5">
      {{ title }}
    </q-item-label>
    <div>
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * A container for settings components.
 */

defineProps({
  title: {
    type: String,
    required: false,
    default: '',
  }
})
</script>