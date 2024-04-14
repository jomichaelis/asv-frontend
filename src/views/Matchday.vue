<template>
  <v-container class="fill-height">
    <v-responsive class="fill-height">
      <div class="main-div">
        <PageTitle title="Matchday-Bilder" />

        <div class="mx-3 mt-3 mb-4">
          <v-card flat>
            <v-card-title class="d-flex align-center">
              <v-btn
                color="primary"
                v-bind="props"
                variant="text"
                prepend-icon="mdi-plus-box"
                class="text-none"
                @click="createManualMatchdayPreview"
              >
                Manuell erstellen
              </v-btn>
              <v-spacer></v-spacer>
            </v-card-title>

            <v-divider></v-divider>

            <v-data-table
              v-model:search="search"
              v-model:sort-by="sortBy"
              :items="matchdayPreviews"
              :headers="headers"
              :items-per-page="20"
              :row-props="itemRowBackground"
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
              <template v-slot:item.home="{ item }">
                <div class="text-center my-2">
                  <v-avatar tile :size="50" class="mb-1">
                    <v-img :src="teamsStore.getByID(item.home)?.wappen_square?.url" />
                  </v-avatar>
                  <p class="text-body-1">{{ teamsStore.getByID(item.home)?.name }} {{ item?.home_team > 1 ? item?.home_team : '' }}</p>
                </div>
              </template>
              <template v-slot:item.guest="{ item }">
                <div class="text-center my-2">
                  <v-avatar tile :size="50" class="mb-1">
                    <v-img :src="teamsStore.getByID(item.guest)?.wappen_square?.url" />
                  </v-avatar>
                  <p class="text-body-1">{{ teamsStore.getByID(item.guest)?.name }} {{ item?.guest_team > 1 ? item?.guest_team : '' }}</p>
                </div>
              </template>
              <template v-slot:item.desktop="{ item }">
                <a
                  :href="item.desktop?.downloadURL"
                  :data-fancybox="item.id"
                  class=""
                >
                  <v-img
                    :width="130"
                    :src=item.desktop?.thumbDownloadURL
                  ></v-img>
                </a>
              </template>
              <template v-slot:item.story="{ item }">
                <a
                  :href="item.story?.downloadURL"
                  :data-fancybox="item.id"
                  class=""
                >
                  <v-img
                    :width="46"
                    :src=item.story?.thumbDownloadURL
                  ></v-img>
                </a>
              </template>
              <template v-slot:item.square="{ item }">
                <a
                  :href="item.square?.downloadURL"
                  :data-fancybox="item.id"
                  class=""
                >
                  <v-img
                    :height="80"
                    :src=item.square?.thumbDownloadURL
                  ></v-img>
                </a>
              </template>
              <template v-slot:item.kickoff="{ item }">
                <span class="font-weight-bold text-body-1">
                  {{ format(item.kickoff?.toDate(), 'EE d. MMMM yy - HH:mm', { locale: de }) }}
                  <v-chip v-if="isSoon(item.kickoff?.toDate())" label color="primary" variant="elevated" class="ml-2">
                    bald
                  </v-chip>
                </span>
              </template>
              <template v-slot:item.actions="{ item }">
                <v-tooltip location="start" text="Team löschen">
                  <template v-slot:activator="{ props: tooltipProps }">
                    <v-icon
                      ref="activatorRef"
                      v-bind="tooltipProps"
                      class="me-2"
                      @click="onDelete(item.id)"
                    >
                      mdi-delete
                    </v-icon>
                  </template>
                </v-tooltip>
              </template>
            </v-data-table>
          </v-card>
        </div>
      </div>
    </v-responsive>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { format, differenceInDays, differenceInSeconds } from 'date-fns'
import { de } from 'date-fns/locale'
import { useConfirm } from 'vuetify-use-dialog'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'
import { Fancybox } from "@fancyapps/ui"
import "@fancyapps/ui/dist/fancybox/fancybox.css"

import PageTitle from '@/components/PageTitle.vue'
import DialogTeamNew from '@/components/verwaltung/teams/DialogTeamNew.vue'
import DialogTeamEdit from '@/components/verwaltung/teams/DialogTeamEdit.vue'
import ButtonTeamDelete from '@/components/verwaltung/teams/ButtonTeamDelete.vue'

import { useTeamsStore } from '@/store/teams'
import { useMatchdayPreviewsStore } from '@/store/matchdayPreviews'

const createConfirm = useConfirm()

const teamsStore = useTeamsStore()
const matchdayPreviewsStore = useMatchdayPreviewsStore()

const props = defineProps({
  asvOnly: {
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

const search = ref('')

const sortBy = ref([{ key: 'kickoff', order: 'desc' }])

const headers = ref([
  { title: 'Heimteam', key: 'home', sortable: false, align: 'center' },
  { title: 'Auswärtsteam', key: 'guest', sortable: false, align: 'center' },
  { title: 'Desktop', key: 'desktop', sortable: false },
  { title: 'Story', key: 'story', sortable: false },
  { title: 'Quadratisch', key: 'square', sortable: false },
  { title: 'Anstoß', key: 'kickoff', order: 'desc' },
  { title: 'Aktionen', key: 'actions', sortable: false, align: 'end'}
])

const matchdayPreviews = computed(() => {
  return matchdayPreviewsStore.getAll
})

const isSoon = (date) => {
  const diff = differenceInDays(new Date(Date.now() + 3*24*60*60*1000), date)
  return diff < 3 && diff > -1
}

const itemRowBackground = (row) => {
  const diff = isSoon(row.item.kickoff.toDate())
  let rowClasses = diff ? 'soon-row ' : ''
  if (row.item.id === nextID.value) {
    rowClasses += 'next-row'
  }
  return { class: rowClasses }
}

const download = (url) => {
  var xhr = new XMLHttpRequest();
  xhr.responseType = 'blob';
  xhr.onload = (event) => {
    let blob = xhr.response;
    let a = document.createElement('a');
    a.href = window.URL.createObjectURL(blob); // xhr.response is a blob
    a.download = url.split("/").pop(); // Set the file name.
    a.style.display = 'none';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };
  xhr.open('GET', url);
  xhr.send();
}

const nextID = computed(() => {
  return matchdayPreviewsStore.getAll?.map((item) => {
    console.log({
      diff: differenceInSeconds(new Date(), item.kickoff.toDate()),
      id: item.id
    })?.filter((item) => item.diff < 0)

    return {
      diff: differenceInSeconds(new Date(), item.kickoff.toDate()),
      id: item.id
    }})?.filter((item) => item.diff < 0)?.sort((a, b) => b.diff - a.diff)[0]?.id
})

const onDelete = async (matchdayID) => {
  const isConfirmed = await createConfirm({
    title: `Matchday-Bild löschen`,
    content: 'Bist Du sicher?',
  })
  if (!isConfirmed) return

  try {
    await matchdayPreviewsStore.delete(matchdayID)
    toast.success("Match wurde entfernt.")
  } catch (error) {
    console.error(error)
    toast.error("Match konnte nicht entfernt werden.")
  }

}

const createManualMatchdayPreview = () => {
  toast.info("Funktion noch nicht verfügbar.")
}

</script>

<style>
.soon-row {
  background-color: rgba(48, 47, 0, 20) !important;
}
.next-row > td {
  border-bottom: 4px solid rgb(var(--v-theme-primary)) !important;
}
</style>
