import { nextTick, ref } from "vue";
import { FilesBatch, StartResponse } from "src/modules/models";
import { usePredictStore } from "src/stores/predict-store";
import { MediaRecorder, register } from 'extendable-media-recorder';
import { connect } from 'extendable-media-recorder-wav-encoder';

export function useAudio() {
  const devices = ref<MediaDeviceInfo[]>([]);
  const isRecording = ref(false);

  let batches: FilesBatch[] = [];

  const prediction = ref<StartResponse | null>(null);
  const predictStore = usePredictStore();

  const LENGTH_MS = 80;

  const init = async () => {
    isRecording.value = false;
    devices.value = [];
    devices.value = await navigator.mediaDevices.enumerateDevices();
    devices.value = devices.value.filter(device => device.kind === 'audioinput');

    // Register WAV encoder.
    await register(await connect());
  };

  const initBatch = (): FilesBatch => {
    return {
      files: [],
      batchId: Math.random().toString(36).substring(2)
    };
  }

  const startRecording = async () => {
    isRecording.value = true;

    if (devices.value.length === 0) {
      isRecording.value = false;
      throw new Error('No audio devices found');
    }

    let batch: FilesBatch = initBatch();

    for (let device of devices.value) {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          audio: { deviceId: device.deviceId }
        });

        const mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/wav' });

        // Ensure mediaRecorder is stopped before starting a new recording.
        if (mediaRecorder.state === 'recording') {
          mediaRecorder.stop();
        }

        const recordAudio = () => {
          mediaRecorder.start();

          setTimeout(() => {
            if (!isRecording.value) {
              mediaRecorder.stop();
              stream.getTracks().forEach(track => track.stop());
              return;
            }
            mediaRecorder.stop();
          }, LENGTH_MS); // 1 second recording
        };

        // On data available, save the audio file
        mediaRecorder.ondataavailable = (e) => {
          if (!isRecording.value) {
            return;
          }

          const audioBlob = e.data;

          // DEBUG: save the audio file
          //const url = URL.createObjectURL(audioBlob);
          //const a = document.createElement('a');
          //a.href = url;
          //a.download = `audio-${Date.now()}.wav`;
          //a.click();

          // Add to the list of files
          batch.files.push(new File([audioBlob], `audio-${Date.now()}.wav`, {
            type: 'audio/wav'
          }));

          // Do we have enough files to send (should be amount of microphones)
          if (batch.files.length === devices.value.length) {
            const clone = { ...batch };
            if (batches.find(b => b.batchId === clone.batchId)) {
              // Already sent this batch
              return;
            }
            batches.push(batch);

            // Send the batch
            predictStore.predict(clone).then((response) => {
              prediction.value = response;
            });

            // Initialize a new batch
            batch = initBatch();
          }
        };

        mediaRecorder.onstop = () => {
          if (isRecording.value) {
            // Delay to ensure proper intervals between recordings
            setTimeout(recordAudio, LENGTH_MS); // Start new recording after 1 second
          } else {
            stream.getTracks().forEach(track => track.stop());
          }
        };

        recordAudio(); // Start the first recording

      } catch (error) {
        console.error('Error:', error);
      }
    }
  };

  const stopRecording = () => {
    isRecording.value = false;
  };

  init();
  return {
    devices,
    startRecording,
    stopRecording,
    prediction,
    isRecording
  };
}
