// Example of a composable
import { ref } from 'vue';

export function useExampleComposable() {
  const count = ref(0);

  function increment() {
    count.value++;
  }

  return {
    count,
    increment,
  };
}
