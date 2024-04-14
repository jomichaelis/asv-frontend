<template>
  <v-row justify="center" class="my-0">
    <v-hover v-slot="{ isHovering, props }">
      <v-avatar
        color="black"
        rounded="0"
        size="200"
        v-bind="props"
      >
        <v-img cover :src="team?.wappen_square?.url">
          <v-row justify="end" :class="`mt-1 mr-1 avatar-buttons ${isHovering ? 'on-hover' : ''}`">
            <v-menu
              min-width="200px"
              rounded
              offset-y
              location="bottom"
            >
              <template v-slot:activator="{ props }">
                <v-btn
                  rounded="pill"
                  variant="flat"
                  :class="`mr-0`"
                  color="primary"
                  size="x-small"
                  icon
                  v-bind="props"
                >
                  <v-icon size="x-large">
                    mdi-dots-vertical
                  </v-icon>
                </v-btn>
              </template>
              <v-list density="compact">
                <v-list-item v-if="team?.status === 'okay'" @click="uploadForm.click()">
                  <v-list-item-title>Bild ändern</v-list-item-title>
                </v-list-item>
                <v-list-item v-if="team?.status === 'okay'" @click="onRemovePhoto">
                  <v-list-item-title>Bild entfernen</v-list-item-title>
                </v-list-item>
                <v-list-item v-else @click="uploadForm.click()">
                  <v-list-item-title>Bild hinzufügen</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </v-row>
          <div class="avatar-overlay-center">
            <v-progress-circular
              v-if="uploadLoading"
              :value="wappenUploadProgress"
              color="white"
              class="progress-loader"
            ></v-progress-circular>
            <v-icon
              v-if="resizing"
              color="white"
              :size="40"
              class="progress-loader"
            >
              mdi-image-sync-outline
            </v-icon>
          </div>
        </v-img>
      </v-avatar>
    </v-hover>
    <v-file-input
      ref="uploadForm"
      v-model="imageFile"
      accept="image/*"
      class="d-none"
      type="file"
      @change="onFileChanged"
    />
  </v-row>
</template>

<script setup>
import { ref, computed } from 'vue'
import { storage, db } from '@/plugins/firebase'
import { getAuth } from 'firebase/auth'
import { doc, setDoc, onSnapshot } from 'firebase/firestore'
import { ref as fbRef, uploadBytesResumable, getDownloadURL } from 'firebase/storage'
import { format } from 'date-fns'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

import { useTeamsStore } from '@/store/teams'

const teamsStore = useTeamsStore()

const uploadForm = ref(null)
const imageFile = ref(null)

const uploadLoading = ref(false)
const wappenUploadProgress = ref(0)

const resizing = ref(false)

const teamBinding = ref(null)

const props = defineProps({
  teamID: {
    type: String,
    required: true,
  },
})

const team = computed(() => teamsStore.getByID(props.teamID))

const onFileChanged = async () => {
  if(imageFile.value == null) return
  uploadLoading.value = true
  let filename = imageFile.value[0].name
  const date = format(new Date(), 'yyyy-MM-dd-HH-mm-ss')
  filename = `${date}_${filename}`
  const metadata = {
    contentType: imageFile.value[0].type,
    customMetadata: {
      teamID: props.teamID,
      userID: getAuth().currentUser?.uid,
    }
  }

  const storageRef = fbRef(storage, 'wappen/' + filename)
  const uploadTask = uploadBytesResumable(storageRef, imageFile.value[0], metadata)

  uploadTask.on('state_changed',
    (snapshot) => {
      wappenUploadProgress.value = (snapshot.bytesTransferred / snapshot.totalBytes) * 100
      switch (snapshot.state) {
        case 'paused':
          toast.info('Upload wurde pausiert.')
          break;
        case 'running':
          break;
      }
    },
    (error) => {
      switch (error.code) {
        case 'storage/unauthorized':
          toast.error('Du hast keine Berechtigung, um diese Datei hochzuladen.')
          break;
        case 'storage/canceled':
          toast.error('Upload wurde abgebrochen.')
          break;
        case 'storage/unknown':
          toast.error('Ein unbekannter Fehler ist aufgetreten.')
          break;
        default:
          toast.error(error.code)
          break;
      }
      uploadLoading.value = false
    },
    async () => {
      const docRef = doc(db, "teams", props.teamID)
      const payload = {
        wappen: {
          filename: filename,
          url: await getDownloadURL(uploadTask.snapshot.ref),
          path: uploadTask.snapshot.ref.fullPath,
        },
        status: 'resizing'
      }
      await setDoc(docRef, payload, { merge: true })
        .catch((error) => {
          console.error(error)
          toast.error('Fehler beim Setzen des Dokuments.')
        })
      bindTeam()
      resizing.value = true
      uploadLoading.value = false
      setTimeout(() => { wappenUploadProgress.value = 0 }, 1000)
    }
  )
}

const bindTeam = () => {
  const q = doc(db, "teams", props.teamID)
  teamBinding.value = onSnapshot(q, { includeMetadataChanges: true }, async (doc) => {
    const data = doc.data()
    if(data?.status !== 'resizing') {
      await teamsStore.fetchTeam(props.teamID)
      unbindTeam()
      resizing.value = false
    }
  })
}

const unbindTeam = () => {
  teamBinding.value()
}

const onRemovePhoto = async () => {
  const payload = {
    wappen: {},
    wappen_square: {},
    wappen_x160: {},
    status: 'no-image'
  }
  await teamsStore.updateTeam(props.teamID, payload)
    .catch((error) => {
      console.error(error)
      toast.error('Fehler beim Löschen des Bildes.')
      return
    })
  await teamsStore.fetchTeam(props.teamID)
  toast.success('Bild wurde gelöscht.')
}

</script>

<style scoped>
.avatar-buttons {
  opacity: 0;
  transition: opacity 0.2s ease-in-out;
}
.avatar-buttons.on-hover {
  opacity: 1;
}

.avatar-overlay-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>
