<template>
  <v-hover v-slot="{ hover }">
    <v-card color="#eeeeee">
      <v-img
        :src=imageURL
        lazy-src="/lazy_fb.jpg"
      >
        <template v-slot:placeholder>
          <div class="d-flex align-center justify-center fill-height">
            <v-progress-circular
                :indeterminate="true"
                color="grey-lighten-4"
            ></v-progress-circular>
          </div>
        </template>
        <div
          class="d-flex align-center justify-center fill-height white"
          v-if="loading"
        >
          <v-progress-circular
              :indeterminate="true"
              color="grey-lighten-4"
          ></v-progress-circular>
        </div>
        <v-expand-transition>
          <div
            v-if="hover && !loading"
            class="d-flex transition-fast-in-fast-out black v-card--reveal text-h2"
            style="height: 100%;"
          >
            <v-btn
              variant="plain"
              :icon="true"
              size="70"
              @click="download()"
            >
              <v-icon
                  size="50"
                  color="yellow"
              >
                mdi-download
              </v-icon>
            </v-btn>
          </div>
        </v-expand-transition>
      </v-img>
    </v-card>
  </v-hover>
</template>

<script>
import { getStorage, ref, getDownloadURL} from "firebase/storage";
export default {
  name: "MatchdayCard",
  props: {
    imageURL: {
      type: String,
      default: ''
    },
    team: {
      type: Number,
      default: 1
    },
    platform: {
      type: String,
      default: 'facebook'
    },
    loading: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {

    }
  },
  methods: {
    download () {
      const storage = getStorage();
      const httpsReference = ref(storage, this.imageURL);
      getDownloadURL(httpsReference)
        .then((url) => {
          console.log(url)
          // This can be downloaded directly:
          const xhr = new XMLHttpRequest();
          xhr.responseType = 'blob';
          xhr.onload = (event) => {
            const blob = xhr.response;
            let a = document.createElement('a');
            a.href = window.URL.createObjectURL(blob); // xhr.response is a blob
            console.log(this.imageURL.split("/"))
            a.download = this.imageURL.split("/").pop(); // Set the file name.
            a.style.display = 'none';
            document.body.appendChild(a);
            a.click();
          };
          xhr.open('GET', url);
          xhr.send();
        })
    }
  }
}
</script>

<style scoped>
.v-card--reveal {
  align-items: center;
  bottom: 0;
  justify-content: center;
  opacity: .9;
  position: absolute;
  width: 100%;
}
</style>