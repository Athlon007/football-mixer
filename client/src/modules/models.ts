export interface PredictionResponse {
  result: string;
  prediction: number[][];
}

export interface StartResponse {
  batch_id: string;
  message: string;
  best_source: number; // Index of the best source
  best_output: BestOutput;
}

export interface BestOutput {
  result: string;
  prediction: number[][];
}

export interface FilesBatch {
  files: File[];
  batchId: string;
}

export interface SystemStatusResponse {
  status: string;
}

export interface ModelResponse {
  name: string;
  version: string;
  recommended_sampling_rate_ms: number;
  recommended: boolean | undefined;
}

export interface ModelsListResponse {
  current_model: string;
  models: ModelResponse[];
}
