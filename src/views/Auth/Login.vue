<template>
  <v-container class="fill-height">
    <v-responsive class="align-center text-center fill-height mx-2">
      <div class="main-div">
        <v-row justify="center">
          <v-img height="200px" width="200px" src="@/assets/asv-logo200.png" />
        </v-row>

        <div v-if="formState === 'login'" style="height: 300px">
          <v-card
            class="mx-auto mt-10 pa-12 pb-8"
            elevation="8"
            max-width="486"
          >
            <v-form
              ref="form"
              v-model="valid"
              fast-fail
              @submit.prevent
            >
              <v-text-field
                v-model="email"
                density="compact"
                placeholder="E-Mail"
                prepend-inner-icon="mdi-email-outline"
                variant="outlined"
                color="primary"
                autofocus
                required
                autocomplete="email"
                :rules="emailRules"
                class="pb-2"
              ></v-text-field>

              <v-text-field
                v-model="password"
                :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
                :type="visible ? 'text' : 'password'"
                density="compact"
                placeholder="Passwort"
                prepend-inner-icon="mdi-lock-outline"
                variant="outlined"
                color="primary"
                autocomplete="current-password"
                required
                :rules="pwRules"
                @click:append-inner="visible = !visible"
              ></v-text-field>

              <v-btn
                block
                color="primary"
                type="submit"
                variant="tonal"
                :loading="loading"
                :disabled="!valid"
                class="mt-4 mb-3"
                @click="onSignIn"
              >
                Anmelden
              </v-btn>
            </v-form>

            <v-row justify="end" class="mt-0 mb-3">
              <v-col cols="auto" class="py-2">
                <v-btn variant="text" class="text-none" border size="small" @click="formState='pw-reset'">
                  Passwort vergessen?
                </v-btn>
              </v-col>
            </v-row>

            <v-divider color="primary" class="border-opacity-50" />

            <v-btn
              variant="tonal"
              border
              :loading="loadingGoogle"
              :disabled="loadingGoogle"
              class="mt-6"
              @click="onSignInWithGoogle"
            >
            <template v-slot:prepend>
              <img class="mr-1" width="20" height="20" src="@/assets/google.svg" alt="google-logo">
            </template>
              Mit Google anmelden
            </v-btn>
          </v-card>
        </div>

        <div v-else style="height: 300px">
          <v-card
            class="mx-auto mt-10 pa-12 pb-8"
            elevation="8"
            max-width="448"
            rounded="lg"
          >

            <v-text-field
              v-model="email"
              density="compact"
              placeholder="E-Mail"
              prepend-inner-icon="mdi-email-outline"
              variant="outlined"
              color="primary"
            ></v-text-field>

            <v-btn
              block
              color="primary"
              type="submit"
              variant="tonal"
              size="large"
              class="mb-3"
              @click="onResetPW"
            >
              Passwort zurücksetzen
            </v-btn>

            <v-row>
              <v-col class="d-flex align-center justify-start">
                <v-btn
                  variant="text"
                  class="text-primary text-none"
                  x-small
                  @click="formState='login'"
                  prepend-icon="mdi-arrow-left"
                >
                  Anmelden
                </v-btn>
              </v-col>
            </v-row>
          </v-card>
        </div>
      </div>

    </v-responsive>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { signIn, signInWithGoogle } from '@/plugins/firebase'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

const router = useRouter()
const route = useRoute()

const loading = ref(false)
const valid = ref(false)

const visible = ref(false)
const formState = ref('login')

const email = ref('')
const password = ref('')

const loadingGoogle = ref(false)

const emailRules = ref([
  value => {
    if (value) return true
    return 'Bitte gib eine Mail-Adresse an.'
  },
])

const pwRules = ref([
  value => {
    if (value) return true
    return 'Bitte gib ein Passwort an.'
  },
  value => {
    if (value?.length > 9) return true
    return 'Dein Passwort hat mindestens 10 Zeichen.'
  },
])

const onSignIn = async () => {
  loading.value = true
  try {
    await signIn(email.value, password.value)
    router.push(route.query.redirect || { name: 'Home' })
    toast.success('Anmeldung erfolgreich')
  } catch (error) {
    toast.error(`Anmeldung fehlgeschlagen: ${error}`)
  } finally {
    loading.value = false
  }
}

const onSignInWithGoogle = async () => {
  loadingGoogle.value = true
  try {
    await signInWithGoogle()
    router.push(route.query.redirect || { name: 'Home' })
    toast.success('Anmeldung erfolgreich')
  } catch (error) {
    toast.error('Anmeldung fehlgeschlagen')
  } finally {
    loadingGoogle.value = false
  }
}

const onResetPW = () => {
  resetPW(email.value)
}
</script>
