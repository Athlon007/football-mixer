import { defineStore } from "pinia";
import { computed, nextTick, onMounted, ref, watch } from "vue";

export const useSettingsStore = defineStore("settings", () => {
  interface DeviceEntry {
    device: MediaDeviceInfo;
    enabled: boolean;
  }

  const devices = ref<DeviceEntry[]>([]);
  const initialized = ref(false);

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
      initialized.value = true;
      loadSettings();
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
    }
  }

  watch(devices, () => {
    if (initialized.value) {
      localStorage.setItem('settings_devices', JSON.stringify(devices.value));
    }
  }, { deep: true });

  return {
    devices,
    usedDevices,
    moveDeviceUp,
    moveDeviceDown
  };
});
