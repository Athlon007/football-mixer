import { ref } from "vue";
import { socket } from "src/boot/socket";
import { PredictionResponse } from "src/modules/models";

export function useAudio() {
  const devices = ref<MediaDeviceInfo[]>([]);
  const isRecording = ref(false);
  let audioChunks: Blob[] = [];
  let totalAudioDuration = 0;

  const prediction = ref<PredictionResponse | null>(null);

  const init = async () => {
    console.log('init');
    isRecording.value = false;
    devices.value = [];
    devices.value = await navigator.mediaDevices.enumerateDevices();
    devices.value = devices.value.filter(device => device.kind === 'audioinput');

    // DEBUG: only take first device (for now)
    if (devices.value.length > 0) {
      devices.value = [devices.value[0]];
    }
  };

  const startRecording = async () => {
    isRecording.value = true;
    console.log('start recording');

    if (devices.value.length === 0) {
      isRecording.value = false;
      throw new Error('No audio devices found');
    }

    for (let device of devices.value) {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          audio: { deviceId: device.deviceId }
        });

        const sampleRate = stream.getAudioTracks()[0].getSettings().sampleRate;
        const mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.start();

        mediaRecorder.ondataavailable = (e) => {
          audioChunks.push(e.data);

          const chunkDuration = e.data.size / (sampleRate * 2); // Assuming 16-bit audio (2 bytes per sample)
          totalAudioDuration += chunkDuration;

          if (totalAudioDuration >= 3) {
            const audioBlob = new Blob(audioChunks);
            sendAudioData(audioBlob, sampleRate);

            audioChunks = [];
            totalAudioDuration = 0;
          }
        };

        if (mediaRecorder.state === 'recording') {
          mediaRecorder.stop();
        }
        mediaRecorder.start(1000);

      } catch (error) {
        console.error('Error:', error);
      }
    }
  };

  const stopRecording = () => {
    isRecording.value = false;
  };

  const sendAudioData = async (audioBlob: Blob, sampleRate: number) => {
    const arrayBuffer = await audioBlob.arrayBuffer();

    const paddedLength = Math.ceil(arrayBuffer.byteLength / 4) * 4;
    const paddedArrayBuffer = new ArrayBuffer(paddedLength);
    const paddedView = new Uint8Array(paddedArrayBuffer);
    paddedView.set(new Uint8Array(arrayBuffer));

    console.log(paddedArrayBuffer);
    socket.emit('audio_stream', { audioData: paddedArrayBuffer, sampleRate: sampleRate });
  };

  socket.on('prediction', (data: PredictionResponse) => {
    console.log('prediction', data);
    prediction.value = data;
  });

  init();
  return {
    devices,
    startRecording,
    stopRecording,
    sendAudioData,
    prediction,
    isRecording
  };
}
