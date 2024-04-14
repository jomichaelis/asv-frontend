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

  // for (let i = 0; i < asvTeams.value.length; i++) {
  //   loadings.value[i] = true
  //   await loadUpcomingMatch(asvTeams.value[i])
  //   loadings.value[i] = false
  // }

  loadingUpcomingMatches.value = false
}

const loadUpcomingMatch = async (team, idx) => {
  loadings.value[idx] = true
  const fetchUpcomingMatch = httpsCallable(functions, 'fetchUpcomingMatch')
  let res = null
  try {
    res = await fetchUpcomingMatch({ bfvURL: team.bfvURL, teamID: team.id })
  } catch (e) {
    console.error(e)
    toast.error(e.message)
    loadings.value[idx] = false
    return
  }
  let payload = res.data
  payload.kickoff = new Date(payload.date)
  delete payload.date

  // get home team ID
  const homeTeam = teamsStore.getAll?.find(t => t.identifier.includes(payload.home))
  if (!!homeTeam) {
    payload.home = homeTeam.id
  } else {
    console.error('Home team not found', payload.home)
    toast.error(`Heimteam nicht gefunden: ${payload.home}`)
    loadings.value[idx] = false
    return
  }

  // get away team ID
  const guestTeam = teamsStore.getAll?.find(t => t.identifier.includes(payload.guest))
  if (!!guestTeam) {
    payload.guest = guestTeam.id
  } else {
    console.error('Guest team not found', payload.guest)
    toast.error(`Gastteam nicht gefunden: ${payload.guest}`)
    loadings.value[idx] = false
    return
  }

  const matchRef = doc(db, 'next-matches', team.id)
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
