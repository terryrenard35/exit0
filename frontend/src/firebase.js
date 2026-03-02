import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyCs-3ZsMfYf273lR1ucR9Qy-NuN-JoTNxw",
  authDomain: "friendly-cubist-480305-s6.firebaseapp.com",
  projectId: "friendly-cubist-480305-s6",
  storageBucket: "friendly-cubist-480305-s6.firebasestorage.app",
  messagingSenderId: "686219453854",
  appId: "1:686219453854:web:b117ee4e075dce4a1ca28f"
}; 

const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();
