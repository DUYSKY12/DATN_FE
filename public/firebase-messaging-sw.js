// Give the service worker access to Firebase Messaging.
// Note: This script is only used in production or when running in a browser that supports service workers.
importScripts('https://www.gstatic.com/firebasejs/10.7.1/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/10.7.1/firebase-messaging-compat.js');

// Initialize the Firebase app in the service worker by passing in your configuration
// Since this is in the public folder, we can't easily use environment variables. 
// You should replace these with your actual config or let the main app inject them.
firebase.initializeApp({
    apiKey: "AIzaSyDAt1RUPWbtNbuZthC6endLrhPmiv6rVao",
    authDomain: "vueapp-f1f4c.firebaseapp.com",
    projectId: "vueapp-f1f4c",
    storageBucket: "vueapp-f1f4c.firebasestorage.app",
    messagingSenderId: "290844383962",
    appId: "1:290844383962:web:9f12e7d03c4e3faf4163e3"
});

const messaging = firebase.messaging();

// Handle background messages
messaging.onBackgroundMessage((payload) => {
    console.log('[firebase-messaging-sw.js] Received background message ', payload);
    const notificationTitle = payload.notification.title;
    const notificationOptions = {
        body: payload.notification.body,
        icon: '/favicon.ico'
    };

    self.registration.showNotification(notificationTitle, notificationOptions);
});
