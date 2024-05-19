import { ref } from "vue";
import { socket } from "src/boot/socket";
import { PredictionResponse } from "src/modules/models";

export function useAudio() {
  const devices = ref<MediaDeviceInfo[]>([]);
  const isRecording = ref(false);
  let audioChunks: Blob[] = [];

  const prediction = ref<PredictionResponse | null>(null);

  const init = async () => {
    console.log('init');
    isRecording.value = false;
    devices.value = [];
    devices.value = await navigator.mediaDevices.enumerateDevices();
    devices.value.forEach((device) => {
      if (device.kind !== 'audioinput') {
        devices.value.splice(devices.value.indexOf(device), 1);
      }
    });

    // DEBUG: only take first device (for now)
    if (devices.value.length > 0) {
      devices.value = [devices.value[0]];
    }
  };

  const startRecording = async () => {
    isRecording.value = true;
    console.log('start recording');

    if (devices.value.length == 0) {
      isRecording.value = false;
      throw new Error('No audio devices found');
    }


    for (let device of devices.value) {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          audio: { deviceId: device.deviceId }
        });
        // Start recording
        const mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();

        mediaRecorder.ondataavailable = (e) => {
          // Clear previous audio chunks
          audioChunks = [];

          audioChunks.push(e.data);
          if (isRecording) {
            sendAudioData(new Blob(audioChunks));
          }
        };
        // has started already?
        // stop if it's already started
        if (mediaRecorder.state === 'recording') {
          mediaRecorder.stop();
        }
        mediaRecorder.start(1000);

      } catch (error) {
        // User probably denied access to that mic. Skip it!
        console.error('Error:', error);
      }
    }
  }

  const stopRecording = () => {
    isRecording.value = false;
  }

  const sendAudioData = async (audioBlob: Blob) => {
    const arrayBuffer = await audioBlob.arrayBuffer();

    // Ensure the buffer size is a multiple of 4 bytes
    const paddedLength = Math.ceil(arrayBuffer.byteLength / 4) * 4;
    const paddedArrayBuffer = new ArrayBuffer(paddedLength);
    const paddedView = new Uint8Array(paddedArrayBuffer);
    paddedView.set(new Uint8Array(arrayBuffer));

    console.log(paddedArrayBuffer);
    socket.emit('audio_stream', paddedArrayBuffer);
  };


  socket.on('prediction', (data: PredictionResponse) => {
    console.log('prediction', data);
    prediction.value = data;
  })

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
