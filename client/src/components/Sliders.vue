<template>
  <div class="row justify-center">
    <div v-for="(n, index) in settingsStore.usedDevices" :key="index" class="row no-wrap q-my-sm q-mx-lg">
      <div class="col-8">
        <q-slider v-model="micValues[index]" :min="0" :max="50" color="slider-green" vertical reverse class="slider-height" :data-content="index+1"/>
        <div class="q-pt-md">
          <q-badge outline class="text-h5 bg-primary">
            {{ micValues[index]?.toFixed(0) }}
          </q-badge>
        </div>
      </div>
      <div class="label col-4">
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
  writing-mode: sideways-lr;
  text-align: right;
  color: rgb(189, 189, 189);
  width: 20px;
}

.slider-height {
  height: 30vh;
  max-height: 280px;
}

:deep(.q-slider__thumb) {
  width: 30px !important;
  height: 65px;
  border-radius: 3px;
}

:deep(.q-slider__thumb::before) {
  content: attr(data-content);
  width: 30px;
  height: 65px;
  border-radius: 4px;
  background: linear-gradient(#423D4A, #24262C, #423D4A);
  color: rgb(219, 219, 219);
  border: 2px solid #f5f5f5;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.6);
}

:deep(.q-slider__thumb svg) {
  background-color: #ffffff00 !important;
  color: white;
  border-radius: 0px;
  width: 100%;
  height: 3px;
  transform: none;
  border-radius: 2px solid red;
}

:deep(.q-slider__track),
:deep(.q-slider__track--active) {
  width: 7px !important;
  background-color: #1A191D;
  stroke: #131315;
  stroke-width: 4px;
}

:deep(.q-slider__thumb-shape path) {
  visibility: hidden;
}

:deep(.q-slider__thumb-shape.absolute-full) {
  top: 7px;
  width: 30px;
  height: 3px;
  background-color: #fff !important;
  color: white;
  filter: invert(100);
}

:deep(.q-slider__thumb-shape.absolute-full::before) {
  top: 7px;
  width: 30px;
  height: 3px;
  background-color: #fff !important;
  color: white;
  filter: invert(100);
}

:deep(.q-slider__focus-ring)
{
  display: none;
}

:deep(.q-slider--active.q-slider--label .q-slider__thumb-shape) {
  transform: scale(1) !important;
}

:deep(.q-badge) {
  width: 40px;
  height: 30px;
  font-size: 1.1rem;
  background-color: #182126 !important;
  border: 2px solid #ABABAB;
  margin-top: 15px;
}
</style>