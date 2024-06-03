import { onMounted, ref } from "vue";
import { FilesBatch, StartResponse } from "src/modules/models";
import { usePredictStore } from "src/stores/predict-store";
import { MediaRecorder, register } from 'extendable-media-recorder';
import { connect } from 'extendable-media-recorder-wav-encoder';
import { useSettingsStore } from "src/stores/settings-store";

/**
 * Audio processing composable.
 */
export function useAudio() {
  const settingsStore = useSettingsStore();
  const debugDownloadFiles = ref(false);
  const isRecording = ref(false);

  // List of batches of files to send
  let batches: FilesBatch[] = [];

  const prediction = ref<StartResponse | null>(null);
  const predictStore = usePredictStore();

  const DELAY_BEFORE_NEXT_RECORDING = 40;

  const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();

  const playbackQueue: { [batchId: string]: Blob } = {};

  onMounted(async () => {
    isRecording.value = false;

    // Register WAV encoder.
    await register(await connect());
  });

  /**
   * Initialize a new batch of files.
   */
  const initBatch = (): FilesBatch => {
    return {
      files: [],
      batchId: Math.random().toString(36).substring(2)
    };
  };

  /**
   * Start recording session and prediction process.
   */
  const startRecording = async () => {
    isRecording.value = true;

    if (settingsStore.usedDevices.length === 0) {
      isRecording.value = false;
      throw new Error('No audio devices found');
    }

    let batch: FilesBatch = initBatch();

    for (let device of settingsStore.usedDevices) {
      try {
        // Begin recording
        const stream = await navigator.mediaDevices.getUserMedia({
          audio: { deviceId: device.deviceId },
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
          }, settingsStore.sampleRate);
        };

        // On data available, save the audio file and play back the audio from the first microphone
        mediaRecorder.ondataavailable = async (e) => {
          if (!isRecording.value) {
            return;
          }

          const audioBlob = e.data;

          // DEBUG: save the audio file
          if (debugDownloadFiles.value) {
            const url = URL.createObjectURL(audioBlob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `audio-${Date.now()}_${device.label}.wav`;
            a.click();
            return;
          }

          // Add to the list of files
          batch.files.push(new File([audioBlob], `audio-${Date.now()}.wav`, {
            type: 'audio/wav'
          }));

          // Play back the audio from the first microphone
          queuePlayback(batch.batchId, audioBlob);

          // Do we have enough files to send (should be amount of microphones)
          if (batch.files.length === settingsStore.usedDevices.length) {
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
            setTimeout(recordAudio, DELAY_BEFORE_NEXT_RECORDING);
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

  /**
   * Stop the recording session.
   */
  const stopRecording = () => {
    isRecording.value = false;
  };


  const queuePlayback = async (batchId: string, audioBlob: Blob) => {
    const arrayBuffer = await audioBlob.arrayBuffer();
    const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
    const audioBufferSource = audioContext.createBufferSource();
    audioBufferSource.buffer = audioBuffer;
    audioBufferSource.connect(audioContext.destination);
    audioBufferSource.start();
  }

  return {
    startRecording,
    stopRecording,
    prediction,
    isRecording
  };
}
