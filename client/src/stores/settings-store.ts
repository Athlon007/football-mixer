import { defineStore } from "pinia";
import { computed, nextTick, onMounted, ref, watch } from "vue";

/**
 * Store for managing the settings of the application.
 * We use store for this, so that the settings are persisted across the sessions.
 */
export const useSettingsStore = defineStore("settings", () => {
  interface DeviceEntry {
    device: MediaDeviceInfo;
    enabled: boolean;
  }

  const devices = ref<DeviceEntry[]>([]);
  const initialized = ref(false);
  /** Sample rate of the audio. */
  const sampleRate = ref(1000);

  /**
   * Initializes the store by fetching the list of audio devices.
   */
  onMounted(async () => {
    let audioDevices = await navigator.mediaDevices.enumerateDevices();
    audioDevices = audioDevices.filter(device => device.kind === 'audioinput');
    devices.value = audioDevices.map(device => {
      return {
        device: device,
        enabled: true
      };
    });

    nextTick(() => {
      // After initializing the devices, load the settings.
      initialized.value = true;
      //loadSettings();
    });
  })

  /**
   * Returns the list of devices that are enabled.
   * @returns {MediaDeviceInfo[]} List of enabled devices.
   */
  const usedDevices = computed(() => {
    return devices.value.filter(device => device.enabled).map(device => device.device);
  })

  /**
   * Moves the device up in the list.
   * @param index
   */
  const moveDeviceUp = (index: number) => {
    if (index > 0) {
      const device = devices.value[index];
      devices.value.splice(index, 1);
      devices.value.splice(index - 1, 0, device);
    }
  }

  /**
   * Moves the device down in the list.
   */
  const moveDeviceDown = (index: number) => {
    if (index < devices.value.length - 1) {
      const device = devices.value[index];
      devices.value.splice(index, 1);
      devices.value.splice(index + 1, 0, device);
    }
  }

  /**
   * Loads the settings from the local storage.
   * This is called after initializing the devices.
   * This will load the 'enabled' status of the devices and the order of the devices.
   */
  const loadSettings = () => {
    const settingsDevices = localStorage.getItem('settings_devices');
    // Make sure that the device IDs are same as the ones in the current session.
    if (settingsDevices) {
      const devicesArray = JSON.parse(settingsDevices) as DeviceEntry[];
      const deviceIds = devices.value.map(device => device.device.deviceId);
      devices.value = devicesArray.filter(device => deviceIds.includes(device.device.deviceId));

      // Reorder the devices based on the saved order.
      for (let i = 0; i < devicesArray.length; i++) {
        const index = devices.value.findIndex(device => device.device.deviceId === devicesArray[i].device.deviceId);
        if (index !== -1) {
          devices.value.splice(i, 0, devices.value.splice(index, 1)[0]);
        }
      }

      const rate = localStorage.getItem('settings_sample_rate');
      if (rate) {
        sampleRate.value = parseInt(rate);
      }
    }
  }

  /**
   * Observes the devices and saves the settings to the local storage.
   */
  watch(devices, () => {
    if (initialized.value) {
      localStorage.setItem('settings_devices', JSON.stringify(devices.value));
    }
  }, { deep: true });

  /**
   * Returns the labels of the active microphones.
   */
  const micLabels = computed(() => {
    const labels = usedDevices.value.map((n) => n.label.replace('Microphone (', '').replace(')', ''));
    return labels;
  });

  /**
   * Returns the labels of all the microphones.
   */
  const allMicsLabels = computed(() => {
    return devices.value.map((n) => n.device.label.replace('Microphone (', '').replace(')', ''));
  });

  /**
   * Observes the sample rate and saves the settings to the local storage.
   */
  watch(sampleRate, () => {
    localStorage.setItem('settings_sample_rate', sampleRate.value.toString());
  });

  return {
    devices,
    usedDevices,
    moveDeviceUp,
    moveDeviceDown,
    micLabels,
    sampleRate,
    allMicsLabels
  };
});
