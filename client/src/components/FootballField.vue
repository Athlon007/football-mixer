<template>
  <div ref="fieldContainer" class="container">
    <img :src="fieldImage" alt="Football field" class="no-drag" :width="width" :height="height" />
    <svg :width="width" :height="height" class="overlay">
      <g v-for="(square, index) in squares" :key="square.id">
        <rect
          :x="square.x - size / 2"
          :y="square.y - size / 2"
          :width="size"
          :height="size"
          :fill="square.active ? '#7BBF26' : '#1A191D'"
          stroke="white"
          stroke-width="3"
          rx="5"
          @mousedown="onMouseDown($event, square)"
        />
        <text
          :x="square.x"
          :y="square.y"
          :height="size"
          fill="black"
          text-anchor="middle"
          dominant-baseline="middle"
          font-size="28"
          stroke="#474747"
          stroke-width="1px"
        >
          {{ square.id }}
        </text>
      </g>
    </svg>
  </div>
</template>

<script setup lang="ts">
import { useSettingsStore } from 'src/stores/settings-store';
import { ref, onMounted, watch } from 'vue';

const settingsStore = useSettingsStore();

const width = 800;
const height = 400;
const size = 35;  // Size of the squares

const squares = ref([]);

const draggingSquare = ref(null);
const gridSnap = 10;
const fieldImage = ref('src/assets/football-field.png');

const micValues = ref<number[]>([]);
const currentMicValues = ref<number[]>([]);

const fieldContainer = ref<HTMLElement | null>(null);

const props = defineProps<{
  bestMicrophoneIndex: number;
}>();

onMounted(() => {
  initMics();
});

watch(() => settingsStore.usedDevices, () => {
  initMics();
});

const initMics = () => {
  micValues.value = Array(settingsStore.usedDevices.length).fill(0);
  currentMicValues.value = Array(settingsStore.usedDevices.length).fill(0);
  // Redo below so that positions are saved, and on start they are aligned next to each other
  squares.value = Array.from({ length: settingsStore.usedDevices.length }, (_, index) => ({
    id: index + 1, 
    x: 100 + index * 100,
    y: 100,
    active: false,
  }));
};

watch(() => props.bestMicrophoneIndex, (newIndex) => {
  // Set square to active if it's the best microphone
  squares.value.forEach((square, index) => {
    square.active = index === newIndex;
  });
});

const onMouseDown = (event, square) => {
  event.stopPropagation();
  draggingSquare.value = square;
  window.addEventListener('mousemove', onMouseMove);
  window.addEventListener('mouseup', onMouseUp);
};

const onMouseMove = (event) => {
  if (draggingSquare.value && fieldContainer.value) {
    const fieldRect = fieldContainer.value.getBoundingClientRect();
    draggingSquare.value.x = event.clientX - fieldRect.left;
    draggingSquare.value.y = event.clientY - fieldRect.top;

    // Prevent square from going outside the field
    draggingSquare.value.x = Math.max(size / 2, Math.min(width - size / 2, draggingSquare.value.x));
    draggingSquare.value.y = Math.max(size / 2, Math.min(height - size / 2, draggingSquare.value.y));

    // Snap to grid but smaller steps
    draggingSquare.value.x = Math.round(draggingSquare.value.x / gridSnap) * gridSnap;
    draggingSquare.value.y = Math.round(draggingSquare.value.y / gridSnap) * gridSnap;
  }
};

const onMouseUp = () => {
  draggingSquare.value = null;
  window.removeEventListener('mousemove', onMouseMove);
  window.removeEventListener('mouseup', onMouseUp);
};
</script>

<style lang="scss" scoped>
.container {
  height: 50vh;
  position: relative;
}

.no-drag {
  user-select: none;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  overflow: visible;
}

rect {
  pointer-events: all;
}

svg {
  pointer-events: none;
}

.label {
  transform: rotate(-90deg) translateX(-50%);
  text-align: right;
}
</style>