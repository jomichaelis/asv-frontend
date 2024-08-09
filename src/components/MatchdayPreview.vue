<template>
  <v-card variant="tonal" :loading="props.loading">
    <v-row justify="space-evenly" class="mt-3 mb-0 mx-3">
      <v-col cols="12" class="text-center mb-1">
        <p class="text-h6">{{ team?.description }}</p>
        <p class="text-body-2">{{ match?.liga }}</p>
      </v-col>
      <v-col cols="5" class="text-center">
        <v-avatar tile :size="100" class="mb-4">
          <v-img :src="homeTeam?.wappen_square?.url" />
        </v-avatar>
        <p class="text-body-1">{{ homeTeam?.long1 }}</p>
        <p class="text-body-1">{{ homeTeam?.long2 }} {{ match?.home_team > 1 ? match?.home_team : '' }}</p>
      </v-col>
      <v-col cols="2" align-self="center" class="text-h3 font-weight-bold pa-0 text-center">
        :
      </v-col>
      <v-col cols="5" class="text-center">
        <v-avatar tile :size="100" class="mb-4">
          <v-img :src="guestTeam?.wappen_square?.url" />
        </v-avatar>
        <p class="text-body-1">{{ guestTeam?.long1 }}</p>
        <p class="text-body-1">{{ guestTeam?.long2 }} {{ match?.guest_team > 1 ? match?.guest_team : '' }}</p>
      </v-col>
      <v-col cols="12" class="text-h6 text-center py-0">
        <p>{{ date }}</p>
        <p>{{ time }}</p>
      </v-col>
    </v-row>
    <v-card-actions>
      <v-row justify="space-between">
        <v-col v-if="matchdayPreview?.status === 'finished'">
          <v-row justify="start" class="mx-2 my-2">
            <v-col cols="auto" align-self="center" class="pa-1 pe-2 cursor-pointer" :href="matchdayPreview.story?.downloadURL"
              :data-fancybox="matchdayPreview.id">
              <v-img :width="46" :src=matchdayPreview.story?.thumbDownloadURL></v-img>
            </v-col>
            <v-col cols="auto" align-self="center" class="pa-1 pe-2 cursor-pointer" :href="matchdayPreview.square?.downloadURL"
              :data-fancybox="matchdayPreview.id">
              <v-img :width="80" :src=matchdayPreview.square?.thumbDownloadURL></v-img>
            </v-col>
          </v-row>
        </v-col>
        <v-col align-self="center" class="text-center">
          <v-row justify="end" class="mx-2 my-2">
            <v-chip v-if="matchdayPreview?.status === 'finished'" label prepend-icon="mdi-check" variant="tonal"
              color="success" class="mr-2">
              Bilder generiert
            </v-chip>
            <v-btn v-else rounded="pill" variant="outlined" :loading="loadingPreview" :disabled="match?.isLive"
              :prepend-icon="match?.isLive ? 'mdi-record' : 'mdi-image-plus-outline'"
              :color="match?.isLive ? 'error' : 'primary'" class="pl-3 mt-1 mb-2 mr-1 text-none"
              @click="onCreateMatchdayPreview">
              {{ match?.isLive ? 'Spiel läuft' : 'Bilder generieren' }}
            </v-btn>
          </v-row>
        </v-col>
      </v-row>
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { ref, computed } from 'vue'
import { getAuth } from 'firebase/auth'
import { httpsCallable } from 'firebase/functions'
import { functions } from '@/plugins/firebase'
import { format } from 'date-fns'
import { de } from 'date-fns/locale'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'
import { Fancybox } from "@fancyapps/ui"
import "@fancyapps/ui/dist/fancybox/fancybox.css"

import { useTeamsStore } from '@/store/teams'
import { useUpcomingMatchesStore } from '@/store/upcomingMatches'
import { useMatchdayPreviewsStore } from '@/store/matchdayPreviews'

const teamsStore = useTeamsStore()
const upcomingMatchesStore = useUpcomingMatchesStore()
const matchdayPreviewsStore = useMatchdayPreviewsStore()

const props = defineProps({
  id: {
    type: String,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

Fancybox.bind('[data-fancybox]', {
  Toolbar: {
    display: {
      left: [],
      middle: [],
      right: ["download", "close"],
    },
  },
})

const loadingPreview = ref(false)

const match = computed(() => upcomingMatchesStore.getByID(props.id))

const team = computed(() => teamsStore.getByID(props.id))

const homeTeam = computed(() => teamsStore.getByID(match.value?.team_home))
const guestTeam = computed(() => teamsStore.getByID(match.value?.team_guest))

const date = computed(() => {
  if (!!match.value?.kickoff === false) return ''
  return format(match.value?.kickoff?.toDate(), 'EEEE, d. MMMM', { locale: de })
})

const time = computed(() => {
  if (!!match.value?.kickoff === false) return ''
  return format(match.value?.kickoff?.toDate(), 'HH:mm', { locale: de })
})

const dateF = computed(() => {
  if (!!match.value?.kickoff === false) return ''
  return format(match.value?.kickoff?.toDate(), 'dd.MM.yyyy', { locale: de })
})

const day = computed(() => {
  if (!!match.value?.kickoff === false) return ''
  return format(match.value?.kickoff?.toDate(), 'EEEE', { locale: de })
})

const matchdayPreview = computed(() => {
  return matchdayPreviewsStore.getByID(`${homeTeam.value?.id}-${guestTeam.value?.id}-${match.value?.kickoff?.toDate().getTime()}`)
})

const onCreateMatchdayPreview = async () => {
  loadingPreview.value = true
  const matchID = [homeTeam.value?.id, guestTeam.value?.id, match.value?.kickoff?.toDate().getTime()].join('-')
  const payload = {
    home: homeTeam.value?.id,
    guest: guestTeam.value?.id,
    kickoff: match.value?.kickoff?.toDate(),
    status: 'scheduled',
    createdUserID: getAuth().currentUser.uid,
    createdTimestamp: new Date()
  }
  try {
    await matchdayPreviewsStore.set(matchID, payload)
  } catch (error) {
    toast.error('Fehler beim Erstellen des Matchday Previews')
  }

  const createMatchdayPrevew = httpsCallable(functions, 'create_matchday_preview')
  const res = await createMatchdayPrevew({
    matchID: matchID,
    asvID: props.id,
    home_team: match.value?.team_home,
    guest_team: match.value?.team_guest,
    homeWappenPath: homeTeam.value?.wappen_square?.path,
    guestWappenPath: guestTeam.value?.wappen_square?.path,
    day: day.value,
    date: dateF.value,
    time: time.value,
    homeName: homeTeam.value?.name,
    guestName: guestTeam.value?.name
  })

  matchdayPreviewsStore.update(matchID, {
    status: 'finished',
    story: {
      downloadURL: res.data.storyDownloadURL,
      path: res.data.storyPath,
      thumbDownloadURL: res.data.storyThumbDownloadURL,
      thumbPath: res.data.storyThumbPath
    },
    square: {
      downloadURL: res.data.squareDownloadURL,
      path: res.data.squarePath,
      thumbDownloadURL: res.data.squareThumbDownloadURL,
      thumbPath: res.data.squareThumbPath
    }
  })

  loadingPreview.value = false
}

</script>

<style scoped>
.rotate90 {
  transform: rotate(-90deg);
}

.rotate180 {
  transform: rotate(180deg);
}

.cursor-pointer {
  cursor: pointer;
}
</style>
