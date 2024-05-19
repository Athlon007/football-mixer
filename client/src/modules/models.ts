export interface Todo {
  id: number;
  content: string;
}

export interface Meta {
  totalCount: number;
}

export interface TestMessage {
  response: string;
}

export interface PredictionResponse {
  result: string;
  prediction: number[][];
}
