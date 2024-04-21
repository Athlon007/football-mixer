<template>
  <q-page>
    <div class="q-pa-md full-width row justify-center">
      <h2 class="full-width text-center">Test Socket Messages</h2>

      <div>
        <!-- Scroll list-->
        <q-scroll-area class="q-mt-md" style="height: 300px">
          <q-list bordered>
            <q-item v-for="(message, index) in state.messageEvents" :key="index">
              <q-item-section>
                <q-item-label>{{ message.response }}</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-scroll-area>

        <q-input outlined v-model="input" @keyup.enter="onSend" placeholder="Type a message and press Enter" />
        <q-btn @click="onSend" label="Send" color="primary" class="q-mt-md" />
      </div>

    </div>
  </q-page>
</template>

<script setup lang="ts">
import { socket, state } from 'src/boot/socket';
import { ref } from 'vue';

const input = ref('');

const onSend = () => {
  socket.emit('message', input.value);
  input.value = '';
};

</script>

<style lang="scss" scoped>
.q-list {
  height: 100%
}
</style>