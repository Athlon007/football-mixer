<template>
  <q-page>
    <div class="full-width row justify-center q-pt-md q-pb-md">
      <FootballField :best-microphone-index="audio.prediction.value?.best_source ?? -1" />
    </div>

    <div class="text-center fill-height">
      <div class="row justify-center q-pb-xl">
        <div class="button-container">
          <q-btn :color="audio.isRecording.value ? 'grey-10' : 'light-blue-8'" @click="audio.startRecording" class="simple-border">
            <q-icon size="18px" class="q-pr-sm" name="circle" :color="audio.isRecording.value ? 'red' : 'white'" />
            {{ audio.isRecording.value ? "Recording" : "Record" }}
          </q-btn>
          <q-btn :color="audio.isRecording.value ? 'light-blue-8' : 'grey-10'" label="Stop" @click="stopRecording" icon="stop" class="simple-border"/>
        </div>
      </div>

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
.button-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 30px;
}

.fill-height {
  flex: 1;
  /* Allow the div to fill remaining height */
}

.q-page {
  display: flex;
  flex-direction: column;
}

.q-btn {
  width: 140px;
}

.simple-border {
  border: 2px solid #dbdbdb;
  border-radius: 5px;
}
</style>