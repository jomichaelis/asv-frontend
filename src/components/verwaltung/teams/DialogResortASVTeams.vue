<template>
  <v-dialog width="400" >
    <template v-slot:activator="{ props }">
      <v-btn
        v-bind="props"
        variant="text"
        icon="mdi-sort"
        class="pa-0 text-none"
      />
    </template>
    <template v-slot:default="{ isActive }">
      <v-card>
        <v-form
          ref="form"
          v-model="valid"
          :loading="loading"
          lazy-validation
          @submit.prevent="onSave(isActive)"
        >
          <v-card-title class="py-3">
            {{ props.asv ? 'ASV-' : '' }}Team anlegen
          </v-card-title>
          <v-card-text>
            <v-text-field
              v-model="name"
              label="Teamname"
              required
              :rules="nameRules"
              class="pb-2"
            ></v-text-field>
            <v-text-field
              v-if="props.asv"
              v-model="description"
              label="Beschreibung"
              required
              :rules="descriptionRules"
              class="pb-2"
            ></v-text-field>
            <v-text-field
              v-model="long1"
              label="1. Zeile im Bild"
              class="pb-2"
            ></v-text-field>
            <v-text-field
              v-model="long2"
              label="2. Zeile im Bild"
            ></v-text-field>
            <v-text-field
              v-if="props.asv"
              v-model="bfvURL"
              label="BFV-Team-URL"
              class="pb-2"
            ></v-text-field>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-btn
              rounded="pill"
              variant="text"
              class="text-none"
              @click="isActive.value = false"
            >
              Abbrechen
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn
              rounded="pill"
              :disabled="loading || !valid"
              :loading="loading"
              color="primary"
              variant="elevated"
              class="text-none"
              type="submit"
            >
              Anlegen
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
    </template>
  </v-dialog>
</template>

<script setup>
import { ref } from 'vue'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

import { useTeamsStore } from '@/store/teams'

const teamsStore = useTeamsStore()

const loading = ref(false)

const name = ref('')
const description = ref('')
const long1 = ref('')
const long2 = ref('')
const bfvURL = ref('')

const form = ref(null)
const valid = ref(false)

const nameRules = ref([
  value => {
    if (value?.length > 0) return true
    return 'Bitte gib einen Namen für das Team an.'
  },
])

const descriptionRules = ref([
  value => {
    if (value?.length > 0) return true
    return 'Bitte gib eine Beschreibung für das Team an.'
  },
])

const onSave = async (isActive) => {
  loading.value = true
  const { valid } = await form.value?.validate()
  if (!valid) {
    toast.info('Bitte überprüfe deine Angaben.')
    loading.value = false
    return
  }
  let payload = {
    name: name.value,
    long1: long1.value,
    long2: long2.value,
  }
  await teamsStore.addTeam(payload)
  loading.value = false
  form.value?.reset()
  isActive.value = false
  toast.success("Team angelegt.")
}
</script>
