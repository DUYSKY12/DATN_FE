import { initializeApp } from "firebase/app";
import { getMessaging, getToken, onMessage } from "firebase/messaging";

// Lấy cấu hình từ file .env
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
  measurementId: import.meta.env.VITE_FIREBASE_MEASUREMENT_ID
};

// Khởi tạo Firebase
const app = initializeApp(firebaseConfig);

// Khởi tạo Firebase Cloud Messaging (FCM)
const messaging = getMessaging(app);

// Hàm yêu cầu quyền thông báo và lấy FCM Token
export const requestForToken = async () => {
  try {
    const permission = await Notification.requestPermission();
    if (permission === "granted") {
      const currentToken = await getToken(messaging, {
        vapidKey: import.meta.env.VITE_FIREBASE_VAPID_KEY // Cần Key này từ Firebase Console
      });
      if (currentToken) {
        console.log("FCM Token:", currentToken);
        // Bạn có thể gửi token này lên Backend tại đây
        return currentToken;
      } else {
        console.log("Không thể lấy token. Hãy kiểm tra lại cấu hình.");
      }
    }
  } catch (err) {
    console.log("Lỗi khi lấy token:", err);
  }
};

// Hàm lắng nghe tin nhắn khi app đang mở (Foreground)
export const onMessageListener = () =>
  new Promise((resolve) => {
    onMessage(messaging, (payload) => {
      resolve(payload);
    });
  });

export { app, messaging };
