<template>
  <div class="row">
    <div v-for="(n, index) in settingsStore.usedDevices" :key="index" class="col text-center full-height">
      <q-slider v-model="micValues[index]" :min="0" :max="50" color="slider-green" vertical reverse/>
      <div class="q-pt-md">
        <q-badge outline class="text-h5 bg-primary">
          {{ micValues[index]?.toFixed(0) }}
        </q-badge>
      </div>

      <div class="label">
        {{ settingsStore.micLabels[index] }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useSettingsStore } from 'src/stores/settings-store';
import { onMounted, ref, watch } from 'vue';

const settingsStore = useSettingsStore();

const props = defineProps<{
  bestMicrophoneIndex: number;
}>();

const micValues = ref<number[]>([]);
const currentMicValues = ref<number[]>([]);
const transitionDuration = 2000; // Duration of transition in milliseconds
const fps = 60; // Frames per second
const totalFrames = (transitionDuration / 1000) * fps;

onMounted(() => {
  initMics();
});

watch(() => settingsStore.usedDevices, () => {
  // For now, set all others to 0 and the best one to 50
  initMics();
});

const initMics = () => {
  micValues.value = Array(settingsStore.usedDevices.length).fill(0);
  currentMicValues.value = Array(settingsStore.usedDevices.length).fill(0);
};

watch(() => props.bestMicrophoneIndex, (newIndex) => {
  micValues.value = micValues.value.map((_, index) => (index === newIndex ? 50 : 0));
  return;

  // For now, set all others to 0 and the best one to 50
  let frame = 0;

  const startValues = [...currentMicValues.value];
  const endValues = micValues.value.map((_, index) => (index === newIndex ? 50 : 0));

  const animate = () => {
    if (frame < totalFrames) {
      frame++;
      currentMicValues.value = currentMicValues.value.map((startValue, index) => {
        const endValue = endValues[index];
        const progress = frame / totalFrames;
        return startValue + (endValue - startValue) * progress;
      });

      micValues.value = [...currentMicValues.value];

      requestAnimationFrame(animate);
    }
  };

  animate();
});

// publish method for resetting the sliders
const resetSliders = () => {
  initMics();
};

// expose the method to the parent component
defineExpose({
  resetSliders,
});
</script>

<style lang="scss" scoped>
.label {
  // rotate the text
  transform: rotate(-90deg) translateX(-50%);
  text-align: right;
}

:deep(.q-slider__thumb) {
  width: 10px; // Adjust width as needed
  height: 50px; // Adjust height as needed
  border-radius: 3px; // Rounded corners
  background-color: #00ffff; // Thumb color
}

:deep(.q-slider__thumb::before) {
  content: '';
  width: 30px; // Adjust inner circle width as needed
  height: 65px; // Adjust inner circle height as needed
  border-radius: 3px; // Make it a circle
  background: linear-gradient(#423D4A, #24262C, #423D4A); // Inner circle color
  stroke: #24262C;
  stroke-width: 2px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

:deep(.q-slider__track),
:deep(.q-slider__track--active) {
  width: 6px !important;
  background-color: #1A191D;
  stroke: #131315;
  stroke-width: 4px;
}

:deep(.q-slider__thumb-shape) {
  background-color: white !important;
  border-radius: 0px;
  width: 100%; // Adjust width as needed
  height: 3px; // Adjust height as needed
  transform: none;
}

:deep(.q-slider__thumb-shape::before) {
  background-color: white !important;
  border-radius: 0px;
  width: 100%; // Adjust width as needed
  height: 3px; // Adjust height as needed
  transform: none;
}

:deep(.q-slider__thumb-shape svg) {
  visibility: hidden;
}
</style>