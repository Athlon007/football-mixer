<template>
  <div ref="fieldContainer" class="container">
    <img :src="fieldImage" alt="Football field" class="no-drag" :width="width" :height="height" draggable="false"/>
    <svg :width="width" :height="height" class="overlay">
      <g v-for="(square, index) in squares" :key="index">
        <g v-if="square.enabled">
          <rect
            :x="square.x - size / 2"
            :y="square.y - size / 2"
            :width="size"
            :height="size"
            :fill="square.active ? '#7BBF26' : '#1A191D'"
            :stroke="square.active ? '#7BBF26' : '#FFFFFF'"
            stroke-width="3"
            rx="5"
            @mousedown="onMouseDown($event, square)"
          />
          <text
            :x="square.x"
            :y="square.y + 2"
            :height="size"
            fill="white"
            text-anchor="middle"
            dominant-baseline="middle"
            font-size="28"
            font-weight="bold"
            stroke="#474747"
            stroke-width="1px"
          >
          {{ square.labelIndex }}
        </text>
        </g>
      </g>
    </svg>
  </div>
</template>

<script setup lang="ts">
import { useSettingsStore } from 'src/stores/settings-store';
import { ref, onMounted, watch } from 'vue';

const settingsStore = useSettingsStore(); // Settings store

const width = 600; // Width of the field
const height = 350; // Height of the field
const size = 35;  // Size of the squares

const squares = ref([]); // Array of squares

const draggingSquare = ref(null); // Square being dragged
const gridSnap = 10; // Snap to grid
const fieldImage = ref('src/assets/football-field.png'); // Field image

const fieldContainer = ref<HTMLElement | null>(null); // Field container

// Define props
const props = defineProps<{
  bestMicrophoneIndex: number;
}>();

// Load square positions when component is mounted
onMounted(() => {
  loadSquarePositions();
});

// Load square positions from local storage
const loadSquarePositions = () => {
  const savedPositions = localStorage.getItem('square_positions');
  if (savedPositions) {
    const positions = JSON.parse(savedPositions);
    squares.value = positions.map((pos, index) => ({
      id: pos.id || index + 1,
      x: pos.x || 100 + index * 100,
      y: pos.y || 100,
      active: false,
      enabled: pos.enabled !== undefined ? pos.enabled : settingsStore.usedDevices[index]?.enabled || false,
      labelIndex: pos.labelIndex || null,
    }));
  } else {
    // Initialize squares if no positions are saved
    squares.value = settingsStore.usedDevices.map((device, index) => ({
      id: index + 1,
      x: 100 + index * 100,
      y: 100,
      active: false,
      enabled: device.enabled,
      labelIndex: null,
    }));
  }
};

// Update squares based on used devices
const updateSquares = () => {
  let labelIndex = 1;
  squares.value = settingsStore.devices.map((device, index) => {
    const existingSquare = squares.value.find(sq => sq.id === index + 1) || {
      id: index + 1,
      x: 100 + index * 100,
      y: 100,
      active: false,
      enabled: device.enabled,
      labelIndex: null,
    };

    const newSquare = {
      ...existingSquare,
      enabled: device.enabled,
    };

    if (device.enabled) {
      newSquare.labelIndex = labelIndex++;
    } else {
      newSquare.labelIndex = null;
    }

    return newSquare;
  });
  saveSquarePositions();
};


// Save square positions to local storage
const saveSquarePositions = () => {
  localStorage.setItem('square_positions', JSON.stringify(squares.value));
};

// Update squares when used devices change
watch(() => settingsStore.usedDevices, updateSquares, {deep : true});

// Update squares when best microphone index changes
watch(() => props.bestMicrophoneIndex, (newIndex) => {
  // Set square to active if it's the best microphone
  squares.value.forEach((square, index) => {
    square.active = index === newIndex;
  });
});

// Start dragging square
const onMouseDown = (event: MouseEvent, square: any) => {
  event.stopPropagation();
  draggingSquare.value = square;
  window.addEventListener('mousemove', onMouseMove);
  window.addEventListener('mouseup', onMouseUp);
};

// Move square when dragging within the field
const onMouseMove = (event: MouseEvent) => {
  if (draggingSquare.value && fieldContainer.value) {
    const fieldRect = fieldContainer.value.getBoundingClientRect();
    draggingSquare.value.x = event.clientX - fieldRect.left;
    draggingSquare.value.y = event.clientY - fieldRect.top;

    // Prevent square from going outside the field
    draggingSquare.value.x = Math.max(size / 2, Math.min(width - size / 2, draggingSquare.value.x));
    draggingSquare.value.y = Math.max(size / 2, Math.min(height - size / 2, draggingSquare.value.y));

    // Snap to grid
    draggingSquare.value.x = Math.round(draggingSquare.value.x / gridSnap) * gridSnap;
    draggingSquare.value.y = Math.round(draggingSquare.value.y / gridSnap) * gridSnap;
  }
};

// Stop dragging when mouse is released
const onMouseUp = () => {
  draggingSquare.value = null;
  window.removeEventListener('mousemove', onMouseMove);
  window.removeEventListener('mouseup', onMouseUp);
  saveSquarePositions();
};
</script>

<style lang="scss" scoped>
.container {
  height: 100%;
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