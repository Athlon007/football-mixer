import { defineStore } from 'pinia';
import { api } from 'src/boot/axios';
import { FilesBatch, StartResponse } from 'src/modules/models';

/**
 * Store for managing the predict API.
 */
export const usePredictStore = defineStore('predict', () => {
  const method = 'predict';

  /**
   * Predict the files in the batch.
   */
  const predict = async (batch: FilesBatch): Promise<StartResponse> => {
    // Files cannot be sent over JSON, so we use FormData.
    const formData = new FormData();
    for (let i = 0; i < batch.files.length; i++) {
      formData.append('file', batch.files[i]);
    }
    formData.append('batch_id', batch.batchId);

    const response = await api.post(`/${method}/start`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  }

  return {
    predict,
  };
});
