<template>
  <v-dialog v-model="showDialog" width="400">
    <template v-slot:activator>
      <v-tooltip location="start" text="Team bearbeiten">
        <template v-slot:activator="{ props: tooltipProps }">
          <v-icon
            ref="activatorRef"
            v-bind="tooltipProps"
            class="me-2"
            @click="showDialog = true"
          >
            mdi-pencil
          </v-icon>
        </template>
      </v-tooltip>
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
          <v-card-title>
            Team bearbeiten
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
              label="1. Zeile"
              class="pb-2"
            ></v-text-field>
            <v-text-field
              v-model="long2"
              label="2. Zeile"
            ></v-text-field>
            <v-text-field
              v-if="props.asv"
              v-model="bfvURL"
              label="BFV-Team-URL"
              class="pb-2"
            ></v-text-field>
            <v-combobox
              v-model="identifier"
              label="Identifier (bfv)"
              chips
              multiple
            ></v-combobox>
            <WappenUpload :teamID="props.team?.id" />
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
              Speichern
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
    </template>
  </v-dialog>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

import WappenUpload from '@/components/WappenUpload.vue'

import { useTeamsStore } from '@/store/teams'
import { id } from 'date-fns/locale'

const teamsStore = useTeamsStore()

const props = defineProps({
  team: {
    name: Object,
    required: true
  },
  asv: {
    type: Boolean,
    required: true,
  }
})

const showDialog = ref(false)

const loading = ref(false)

const name = ref('')
const description = ref('')
const long1 = ref('')
const long2 = ref('')
const bfvURL = ref('')
const identifier = ref([])

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

onMounted(() => {
  name.value = props.team?.name || ''
  description.value = props.team?.description || ''
  long1.value = props.team?.long1 || ''
  long2.value = props.team?.long2 || ''
  bfvURL.value = props.team?.bfvURL || ''
  identifier.value = props.team?.identifier || []
})

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
    isASV: props.asv,
    identifier: identifier.value
  }
  if (props.asv) {
    payload = {
      ...payload,
      description: description.value,
      bfvURL: bfvURL.value,
    }
  }
  await teamsStore.updateTeam(props.team.id, payload)
  toast.success("Änderungen gepeichert.")
  loading.value = false
  isActive.value = false
}
</script>
