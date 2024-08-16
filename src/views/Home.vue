<template>
  <v-container class="fill-height">
    <v-responsive class="fill-height">
      <div class="main-div">
        <PageTitle title="Anstehende Spiele" />

        <v-row justify="start" class="mx-0 pt-0 px-3 pb-4">
          <v-tooltip text="lädt Partien von BFV.de">
            <template v-slot:activator="{ props }">
              <v-btn
                rounded="pill"
                v-bind="props"
                variant="outlined"
                color="primary"
                :loading="loadingUpcomingMatches"
                prependIcon="mdi-refresh"
                class="mr-4 mb-4 text-none"
                @click="reloadUpcomingMatches"
              >
                Aktualisieren
              </v-btn>
            </template>
          </v-tooltip>

        </v-row>

        <v-row class="mx-0 mt-3 mb-4">
          <v-col v-for="(match, idx) in upcomingMatches" :key="match.id" cols="12" md="6">
            <MatchdayPreview :id="match.id" :loading="loadings[idx]" />
          </v-col>
        </v-row>
      </div>
    </v-responsive>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { httpsCallable } from 'firebase/functions'
import { db, functions } from '@/plugins/firebase'
import { doc, setDoc, Timestamp } from 'firebase/firestore'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

import PageTitle from '@/components/PageTitle.vue'
import MatchdayPreview from '@/components/MatchdayPreview.vue'

import { useTeamsStore } from '@/store/teams'
import { useUpcomingMatchesStore } from '@/store/upcomingMatches'

const teamsStore = useTeamsStore()
const upcomingMatchesStore = useUpcomingMatchesStore()

const loadingUpcomingMatches = ref(false)

console.log(import.meta.env)

const asvTeams = computed(() => teamsStore.getAllSorted)
const upcomingMatches = computed(() => upcomingMatchesStore.getAll?.sort((a, b) => {
  const aTeam = asvTeams.value.find(t => t.id === a.id)
  const bTeam = asvTeams.value.find(t => t.id === b.id)
  return aTeam?.order - bTeam?.order
}))

const loadings = ref(new Array(100).fill(false))

const reloadUpcomingMatches = async () => {
  loadingUpcomingMatches.value = true

  const asvTeams = computed(() => teamsStore.getAllSorted?.filter(team => team.isASV))

  let promises = []

  for (let i = 0; i < asvTeams.value.length; i++) {
    promises.push(loadUpcomingMatch(asvTeams.value[i], i))
  }
  await Promise.all(promises)

  loadingUpcomingMatches.value = false
}

const loadUpcomingMatch = async (team, idx) => {
  const GetNextMatches = httpsCallable(functions, 'get_next_matches')
  console.log(GetNextMatches)
  let res = null
  try {
    res = await GetNextMatches({ teamURL: team.teamURL })
  } catch (e) {
    console.error(e)
    toast.error(e.message)
    loadings.value[idx] = false
    return
  }
  let payload = res.data
  payload.kickoff = new Date(payload.timestamp)
  delete payload.timestamp
  const upcomingMatchID = payload.id
  delete payload.id

  const matchRef = doc(db, 'upcoming_matches', upcomingMatchID)
  try {
    await setDoc(matchRef, payload)
  } catch (e) {
    console.error(e)
    toast.error('Fehler beim Laden der nächsten Spiele')
    loadings.value[idx] = false
    return
  }
  loadings.value[idx] = false
}

</script>
