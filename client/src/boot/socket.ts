import { io } from 'socket.io-client';
import { TestMessage } from 'src/modules/models';
import { reactive } from 'vue';

export const state = reactive({
  connected: false,
  messageEvents: [] as TestMessage[],
});

export const socket = io(import.meta.env.VITE_API_URL, {
  autoConnect: true,
});


socket.on('connect', () => {
  state.connected = true;
});

socket.on('disconnect', () => {
  state.connected = false;
});

socket.on('message_response', (message: TestMessage) => {
  state.messageEvents.push(message);
});
