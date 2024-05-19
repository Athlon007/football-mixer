<template>
  <q-page>
    <audio-recorder />

    <div class="full-width row justify-center q-pt-md">
      <football-field />
    </div>

    <div class="full-width row justify-center q-pb-xl">
      <div>
        Recording: {{ audio.isRecording.value }}
      </div>

      <div class="q-gutter-x-md col-12 text-center">
        <q-btn label="Start" color="primary" class="q-mt-md" @click="audio.startRecording()" />
        <q-btn label="Stop" color="primary" class="q-mt-md" @click="audio.stopRecording()" />
      </div>

      <div>
        {{ audio.prediction.value }}
      </div>

      <div>
        <div v-for="device in audio.devices.value" :key="device.deviceId">
          {{ device.label }}
        </div>
      </div>

    </div>

    <div class="full-width">
      <sliders />
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Meta } from 'src/modules/models';
import { useAudio } from 'src/composables/audio';
import FootballField from 'src/components/FootballField.vue';
import Sliders from 'src/components/Sliders.vue';

const audio = useAudio();

const meta = ref<Meta>({
  totalCount: 1200
});
</script>