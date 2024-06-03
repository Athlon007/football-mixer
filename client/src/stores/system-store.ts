import { defineStore } from 'pinia';
import { SystemStatusResponse } from 'src/modules/models';
import { api } from 'src/boot/axios';
export const useSystemStore = defineStore('system', () => {
  const method = 'system';

  /**
   * Check the system status
   * @returns SystemStatusResponse
   */
  const check = async (): Promise<SystemStatusResponse> => {
    const response = await api.get(`/${method}/status`);
    return response.data;
  };

  return {
    check,
  };
});
