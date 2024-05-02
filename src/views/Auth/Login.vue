<template>
  <v-container class="fill-height">
    <v-responsive class="align-center text-center fill-height mx-2">
      <div class="main-div">
        <v-row justify="center">
          <v-img height="160px" width="160px" src="@/assets/asv-logo200.png" />
        </v-row>

        <!-- == START == -->
        <div v-if="formState === 'start'">
          <v-card
            class="mx-auto mt-10 pa-12"
            elevation="8"
            max-width="486"
          >

            <v-btn
              variant="flat"
              :loading="loadingGoogle"
              :disabled="loadingGoogle"
              color="white"
              rounded="pill"
              class="text-none w-100 mb-4"
              @click="onSignInWithGoogle"
            >
              <template v-slot:prepend>
                <img class="mr-1" width="20" height="20" src="@/assets/google.svg" alt="google-logo">
              </template>
              Mit Google registrieren
            </v-btn>

            <v-btn
              rounded="pill"
              variant="elevated"
              color="primary"
              class="text-none w-100"
              @click="formState = 'register'"
            >
              Account erstellen
            </v-btn>

            <v-divider color="primary" class="border-opacity-50 my-8" />

            <v-btn
              rounded="pill"
              variant="tonal"
              color="primary"
              class="text-none w-100"
              @click="formState = 'login'"
            >
              Anmelden
            </v-btn>

          </v-card>
        </div>

        <!-- == LOGIN == -->
        <div v-else-if="formState === 'login'">
          <v-card
            class="mx-auto mt-10 pa-12"
            elevation="8"
            max-width="486"
          >

            <v-btn
              variant="flat"
              :loading="loadingGoogle"
              :disabled="loadingGoogle"
              color="white"
              rounded="pill"
              class="text-none w-100"
              @click="onSignInWithGoogle"
            >
              <template v-slot:prepend>
                <img class="mr-1" width="20" height="20" src="@/assets/google.svg" alt="google-logo">
              </template>
              Mit Google anmelden
            </v-btn>

            <v-divider color="primary" class="border-opacity-50 my-8" />

            <v-form
              ref="formLogin"
              v-model="validLogin"
              fast-fail
              @submit.prevent="onSignIn"
            >
              <v-text-field
                v-model="emailLogin"
                density="compact"
                placeholder="E-Mail"
                prepend-inner-icon="mdi-email-outline"
                variant="outlined"
                color="primary"
                autofocus
                required
                autocomplete="email"
                :rules="emailRulesLogin"
                class="pb-2"
              ></v-text-field>

              <v-text-field
                v-model="passwordLogin"
                :append-inner-icon="visibleLogin ? 'mdi-eye-off' : 'mdi-eye'"
                :type="visibleLogin ? 'text' : 'password'"
                density="compact"
                placeholder="Passwort"
                prepend-inner-icon="mdi-lock-outline"
                variant="outlined"
                color="primary"
                autocomplete="current-password"
                required
                :rules="pwRulesLogin"
                @click:append-inner="visibleLogin = !visibleLogin"
              ></v-text-field>

              <v-btn
                block
                color="primary"
                type="submit"
                variant="tonal"
                :loading="loadingLogin"
                :disabled="!validLogin"
                rounded="pill"
                class="text-none mt-2"
              >
                Anmelden
              </v-btn>
            </v-form>

            <v-row justify="space-between" class="mt-7 mb-0">
              <v-col cols="auto" class="py-0">
                <v-btn class="text-none" border size="x-small" icon="mdi-arrow-left" @click="formState='start'">
                </v-btn>
              </v-col>
              <v-col cols="auto" class="py-0">
                <v-btn variant="text" class="text-none" border size="small" rounded="pill" @click="formState='pw-reset'">
                  Passwort vergessen?
                </v-btn>
              </v-col>
            </v-row>
          </v-card>
        </div>

        <!-- == REGISTER == -->
        <div v-else-if="formState === 'register'">
          <v-card
            class="mx-auto mt-10 pa-12"
            elevation="8"
            max-width="486"
          >

            <v-form
              ref="formRegister"
              v-model="validRegister"
              fast-fail
              @submit.prevent="onSignUp"
            >
              <v-text-field
                v-model="emailRegister"
                density="compact"
                placeholder="E-Mail"
                prepend-inner-icon="mdi-email-outline"
                variant="outlined"
                color="primary"
                autofocus
                required
                autocomplete="email"
                :rules="emailRulesRegister"
                class="pb-2"
              ></v-text-field>

              <v-text-field
                v-model="passwordRegister1"
                :append-inner-icon="visibleRegister ? 'mdi-eye-off' : 'mdi-eye'"
                :type="visibleRegister ? 'text' : 'password'"
                density="compact"
                placeholder="Passwort"
                prepend-inner-icon="mdi-lock-outline"
                variant="outlined"
                color="primary"
                required
                :rules="pwRulesRegister1"
                @click:append-inner="visibleRegister = !visibleRegister"
              ></v-text-field>

              <v-text-field
                v-model="passwordRegister2"
                :append-inner-icon="visibleRegister ? 'mdi-eye-off' : 'mdi-eye'"
                :type="visibleRegister ? 'text' : 'password'"
                density="compact"
                placeholder="Passwort wiederholen"
                prepend-inner-icon="mdi-lock-outline"
                variant="outlined"
                color="primary"
                required
                :rules="pwRulesRegister2"
                @click:append-inner="visibleRegister = !visibleRegister"
              ></v-text-field>

              <v-btn
                block
                color="primary"
                type="submit"
                variant="tonal"
                :loading="loadingRegister"
                :disabled="!validRegister"
                rounded="pill"
                class="text-none mt-2"
              >
                Anmelden
              </v-btn>
            </v-form>

            <v-row justify="space-between" class="mt-7 mb-0">
              <v-col cols="auto" class="py-0">
                <v-btn class="text-none" border size="x-small" icon="mdi-arrow-left" @click="formState='start'">
                </v-btn>
              </v-col>
            </v-row>
          </v-card>
        </div>

        <!-- == RESET PASSWORD == -->
        <div v-else-if="formState === 'pw-reset'">
          <v-card
            class="mx-auto mt-10 pa-12 pb-8"
            elevation="8"
            max-width="448"
            rounded="lg"
          >

            <v-form
              ref="formPWReset"
              v-model="validPWReset"
              fast-fail
              @submit.prevent="onResetPassword"
            >
              <v-text-field
                v-model="emailPWReset"
                density="compact"
                placeholder="E-Mail"
                prepend-inner-icon="mdi-email-outline"
                variant="outlined"
                color="primary"
                autofocus
                required
                autocomplete="email"
                :rules="emailRulesPWReset"
              ></v-text-field>

              <v-btn
                block
                color="primary"
                type="submit"
                variant="tonal"
                :loading="loadingPWReset"
                :disabled="!validPWReset"
                rounded="pill"
                class="text-none mt-2"
              >
                Passwort-E-Mail anfordern
              </v-btn>
            </v-form>

            <v-row justify="space-between" class="mt-7 mb-0">
              <v-col cols="auto" class="py-0">
                <v-btn class="text-none" border size="x-small" icon="mdi-arrow-left" @click="formState='login'">
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
import { signIn, signUp, signInWithGoogle, resetPW } from '@/plugins/firebase'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

const router = useRouter()
const route = useRoute()

const formState = ref('start')

const loadingGoogle = ref(false)

const formLogin = ref(null)
const validLogin = ref(false)
const emailLogin = ref('')
const passwordLogin = ref('')
const visibleLogin = ref(false)
const loadingLogin = ref(false)

const formRegister = ref(null)
const validRegister = ref(false)
const emailRegister = ref('')
const passwordRegister1 = ref('')
const passwordRegister2 = ref('')
const visibleRegister = ref(false)
const loadingRegister = ref(false)

const formPWReset = ref(null)
const validPWReset = ref(false)
const emailPWReset = ref('')
const loadingPWReset = ref(false)

const emailRulesLogin = ref([
  value => {
    if (value) return true
    return 'Bitte gib deine Mail-Adresse an.'
  },
])

const pwRulesLogin = ref([
  value => {
    if (value) return true
    return 'Bitte gib dein Passwort an.'
  },
])

const emailRulesRegister = ref([
  value => {
    if (value) return true
    return 'Bitte gib eine Mail-Adresse an.'
  },
])

const pwRulesRegister1 = ref([
  value => {
    if (value) return true
    return 'Bitte gib ein Passwort an.'
  },
])

const pwRulesRegister2 = ref([
  value => {
    if (value) return true
    return 'Bitte gib ein Passwort erneut an.'
  },
  value => {
    if (value === passwordRegister1.value) return true
    return 'Deine Passwörter stimmen nicht überein.'
  }
])

const emailRulesPWReset = ref([
  value => {
    if (value) return true
    return 'Bitte gib deine Mail-Adresse an.'
  },
])

const onSignIn = async () => {
  loadingLogin.value = true
  try {
    await signIn(emailLogin.value, passwordLogin.value)
    router.push(route.query.redirect || { name: 'Home' })
    toast.success('Anmeldung erfolgreich')
  } catch (error) {
    toast.error(`Anmeldung fehlgeschlagen: ${error.message}`)
  } finally {
    loadingLogin.value = false
  }
}

const onSignUp = async () => {
  loadingRegister.value = true
  try {
    await signUp(emailRegister.value, passwordRegister1.value)
    router.push(route.query.redirect || { name: 'Home' })
    toast.success('Registrierung erfolgreich')
  } catch (error) {
    toast.error(`Registrierung fehlgeschlagen: ${error.message}`)
  } finally {
    loadingRegister.value = false
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

const onResetPassword = async () => {
  try {
    loadingPWReset.value = true
    await resetPW(emailPWReset.value)
    emailLogin.value = emailPWReset.value
    formState.value = 'login'
    formPWReset.value?.reset()
    toast.success('E-Mail zum Zurücksetzen des Passworts wurde versandt.')
  } catch(error) {
    toast.error(`E-Mail-Versand fehlgeschlagen: ${error.message}`)
  } finally {
    loadingPWReset.value = false
  }
}
</script>
