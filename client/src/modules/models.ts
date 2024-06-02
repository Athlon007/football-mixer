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
