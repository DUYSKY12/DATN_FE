<template>
    <router-view />
</template>

<script setup>
import { onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useWebSocketNotifications } from '@/composables/useWebSocket'
import { requestForToken, onMessageListener } from '@/firebase'

const router = useRouter()

// WebSocket connection - tự động kết nối khi user login
const handleNotification = (notification) => {
  console.log('📨 Global notification received:', notification)
  // Có thể emit event hoặc xử lý ở đây nếu cần
}

const { connect, disconnect } = useWebSocketNotifications(handleNotification)

// Kết nối WebSocket và Firebase FCM khi app khởi động
onMounted(() => {
  // 1. Firebase FCM setup
  requestForToken();
  onMessageListener().then((payload) => {
    console.log("🔥 Foreground Message received:", payload);
    // Bạn có thể dùng toast để hiển thị thông báo tại đây
  });

  // 2. WebSocket setup
  const token = localStorage.getItem('token')
  if (token) {
    console.log('🔌 App mounted - Connecting WebSocket...')
    setTimeout(() => {
      connect()
    }, 1000)
  }
})

// Watch token changes để reconnect khi user login/logout
watch(() => localStorage.getItem('token'), (newToken, oldToken) => {
  if (newToken && !oldToken) {
    // User vừa login
    console.log('🔌 User logged in - Connecting WebSocket...')
    setTimeout(() => {
      connect()
    }, 500)
  } else if (!newToken && oldToken) {
    // User vừa logout
    console.log('🔌 User logged out - Disconnecting WebSocket...')
    disconnect()
  }
})

// Cleanup khi app unmount
onUnmounted(() => {
  disconnect()
})
</script>