<template>
  <v-tooltip location="start" text="Team löschen">
    <template v-slot:activator="{ props: tooltipProps }">
      <v-icon
        ref="activatorRef"
        v-bind="tooltipProps"
        class="me-2"
        @click="onDelete"
      >
        mdi-delete
      </v-icon>
    </template>
  </v-tooltip>
</template>

<script setup>
import { ref } from 'vue'
import { useConfirm } from 'vuetify-use-dialog'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

import { useTeamsStore } from '@/store/teams'

const createConfirm = useConfirm()

const teamsStore = useTeamsStore()

const props = defineProps({
  team: Object,
  required: true
})

const loading = ref(false)

const onDelete = async () => {
  const isConfirmed = await createConfirm({
    title: `Team löschen: ${props.team.name || 'Unbekannt'}`,
    content: 'Bist Du sicher?',
  })
  if (!isConfirmed) return

  loading.value = true
  try {
    await teamsStore.deleteTeam(props.team.id)
  } catch (error) {
    console.error(error)
    toast.error("Team konnte nicht entfernt werden.")
  }
  loading.value = false
}
</script>
