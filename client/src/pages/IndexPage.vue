<template>
  <q-page>
    <div class="full-width row justify-center q-pt-md q-pb-md">
      <FootballField :best-microphone-index="audio.prediction.value?.best_source ?? -1"/>
    </div>

    <div class="text-center fill-height">
      <div class="row justify-center q-pb-md q-gutter-x-md">
        <q-btn color="primary" @click="audio.startRecording">
          <q-icon size="18px" class="q-pr-sm" name="circle" :color="audio.isRecording.value ? 'red' : 'white'" />
          Record
        </q-btn>
        <q-btn color="primary" label="Stop" @click="stopRecording" icon="stop" />
      </div>

      <SystemStatusComponent />

      <div class="full-width fill-height q-pt-md">
        <sliders ref="slidersRef" :best-microphone-index="audio.prediction.value?.best_source ?? -1" />
      </div>

      <div v-if="showTranscript" class="q-mt-xl">
        <textarea class="full-width" rows="5" v-model="transcript" placeholder="Transcript" readonly />
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import FootballField from 'src/components/FootballField.vue';
import Sliders from 'src/components/Sliders.vue';
import SystemStatusComponent from 'src/components/misc/SystemStatusComponent.vue';
import { useAudio } from 'src/composables/audio';
import { computed, ref } from 'vue';

const audio = useAudio();
const slidersRef = ref<InstanceType<typeof Sliders> | null>(null);
const showTranscript = ref(false);

const transcript = computed(() => {
  return JSON.stringify(audio.prediction.value, null, 2);
});

const stopRecording = () => {
  audio.stopRecording();
};
</script>

<style scoped>
.fill-height {
  flex: 1; /* Allow the div to fill remaining height */
}

.q-page
{
  display: flex;
  flex-direction: column;
}
</style>