<template>
  <v-card flat class="mt-10">
    <v-card-title class="d-flex align-center pe-2">
      {{ props.asvOnly ? 'ASV-' : '' }}Teams
      <DialogTeamNew :asv="props.asvOnly" />
      <DialogResortASVTeams v-if="props.asvOnly" />
      <v-spacer></v-spacer>

      <v-text-field
        v-model="search"
        density="compact"
        label="Suche"
        prepend-inner-icon="mdi-magnify"
        variant="solo-filled"
        flat
        hide-details
        single-line
        clearable
      ></v-text-field>
    </v-card-title>

    <v-divider></v-divider>

    <v-data-table
      v-model:search="search"
      :items="teams"
      :headers="headers"
      :items-per-page="20"
      no-data-text="Keine Teams gefunden"
    >
      <template v-slot:item.wappen="{ item }">
        <v-avatar tile start :size="56" :color="item.wappen_x160?.url?.length > 0 ? 'transparent' : 'primary'" class="my-2">
          <v-img
            v-if="item.wappen_x160?.url?.length > 0"
            :src="item.wappen_x160?.url"
          >
          </v-img>
          <v-icon v-else :size="32">
            mdi-image-off-outline
          </v-icon>
        </v-avatar>
      </template>
      <template v-slot:item.name="{ item }">
        <span class="font-weight-bold text-body-1">
          {{ item.name }}
        </span>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-row justify="end" class="flex-nowrap ma-0">
          <DialogTeamEdit :team="item" :asv="item.isASV" />
          <ButtonTeamDelete :team="item" />
        </v-row>
      </template>
    </v-data-table>
  </v-card>
</template>

<script setup>

import { ref, computed } from 'vue'

import DialogTeamNew from '@/components/verwaltung/teams/DialogTeamNew.vue'
import DialogTeamEdit from '@/components/verwaltung/teams/DialogTeamEdit.vue'
import ButtonTeamDelete from '@/components/verwaltung/teams/ButtonTeamDelete.vue'
import DialogResortASVTeams from '@/components/verwaltung/teams/DialogResortASVTeams.vue'

import { useTeamsStore } from '@/store/teams'

const teamsStore = useTeamsStore()

const props = defineProps({
  asvOnly: {
    type: Boolean,
    default: false
  }
})

const search = ref('')

const constHeaders = ref([
  { title: 'Wappen', key: 'wappen', sortable: false },
  { title: 'Name', key: 'name' },
  { title: '1. Zeile im Bild', key: 'long1' },
  { title: '2. Zeile im Bild', key: 'long2' },
  { title: 'Aktionen', key: 'actions', sortable: false, align: 'end'}
])

const headers = computed(() => {
  let hdrs = constHeaders.value
  if (props.asvOnly) {
    hdrs.splice(2, 0, { title: 'Beschreibung', key: 'description'})
  }
  return hdrs
})

const teams = computed(() => {
  return teamsStore.getAllSortedByName?.filter(team => team.isASV === props.asvOnly)
})

</script>
