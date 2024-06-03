import { defineStore } from 'pinia';
import { SystemStatusResponse } from 'src/modules/models';
import { api } from 'src/boot/axios';

/**
 * Store for managing the system status.
 */
export const useSystemStore = defineStore('system', () => {
  const method = 'system';

  /**
   * Check the system status.
   * @returns SystemStatusResponse
   */
  const check = async (): Promise<SystemStatusResponse> => {
    const response = await api.get(`/${method}/check`);
    return response.data;
  };

  return {
    check,
  };
});
