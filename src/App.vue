<template>
  <router-view />
</template>

<script setup>
import { auth } from '@/plugins/firebase'
import { onAuthStateChanged } from 'firebase/auth'

import { useAuthStore } from '@/store/auth'

const authStore = useAuthStore()

onAuthStateChanged(auth, async (user) => {
  if (user) {
    authStore.set(user)
  } else {
    authStore.$reset()
  }
})
</script>
