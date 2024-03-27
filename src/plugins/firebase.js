import { initializeApp } from "firebase/app"
import { getFirestore, doc, setDoc, connectFirestoreEmulator } from "firebase/firestore"
import {
  getAuth,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signInWithPopup,
  GoogleAuthProvider,
  signOut as fbSignOut,
  onAuthStateChanged,
  connectAuthEmulator
} from "firebase/auth"
import { getStorage, connectStorageEmulator } from "firebase/storage"
import { getFunctions, connectFunctionsEmulator } from "firebase/functions"

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
  measurementId: import.meta.env.VITE_FIREBASE_MEASUREMENT_ID
}

// init firebase
export const firebaseApp = initializeApp(firebaseConfig)

export const db = getFirestore()
export const auth = getAuth()
export const storage = getStorage()
export const functions = getFunctions(firebaseApp, "europe-west3")

export const getCurrentUser = () => {
  return new Promise((resolve, reject) => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      unsubscribe()
      resolve(user)
    }, reject)
  })
}

export const signIn = async (email, password) => {
  return await signInWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      const user = userCredential.user
      return user
    })
    .catch((error) => {
      console.error(error)
      throw error
    })
}

export const signInWithGoogle = async () => {
  return await signInWithPopup(auth, new GoogleAuthProvider())
    .then((result) => {
      const user = result.user
      return user
    })
    .catch((error) => {
      console.error(error)
      throw error
    })
}

export const signOut = async () => {
  await fbSignOut(auth)
    .catch((error) => {
      console.error(error)
      throw error
    })
}

if (import.meta.env.VITE_FIREBASE_USE_EMULATOR === 'true' && import.meta.env.MODE === 'development') {
  console.log('using firebase emulator')
  connectAuthEmulator(auth, 'http://localhost:9099')
  connectFirestoreEmulator(db, '127.0.0.1', 8080)
  connectFunctionsEmulator(functions, '127.0.0.1', 5001)
  connectStorageEmulator(storage, '127.0.0.1', 9199)
} else { console.log('using firebase production') }
