import { io } from 'socket.io-client';
import { TestMessage } from 'src/modules/models';

export const socket = io(import.meta.env.VITE_API_URL, {
  autoConnect: true,
});
