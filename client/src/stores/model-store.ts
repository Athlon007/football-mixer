import { defineStore } from "pinia";
import { ModelsListResponse } from "src/modules/models";
import { ref } from "vue";
import { api } from "src/boot/axios";

/**
 * Store for managing the model settings of the application.
 */
export const useModelStore = defineStore("model", () => {
  const method = "model";
  const models = ref<ModelsListResponse>()

  /**
   * Fetches the list of models from the server.
   */
  const getModels = async () => {
    const response = await api.get(`/${method}`);
    models.value = response.data;
  }

  /**
   * Sets the current model to the given model name.
   */
  const setModel = async (modelName: string) => {
    const response = await api.post(`/${method}/set`, { model_name: modelName });
    if (models.value) {
      models.value.current_model = response.data.model;
    }
  }

  return {
    models,
    getModels,
    setModel
  };
});
