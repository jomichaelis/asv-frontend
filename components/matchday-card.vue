<template>
  <v-hover v-slot="{ hover }">
    <v-card
        color="#eeeeee"
        v-bind="props"
    >
      <v-img
          :src="`https://asv-api.jomichaelis.de/api/v21/preview-image?team=${team}&platform=${platform}`"
          :lazy-src="`https://asv-api.jomichaelis.de/api/v21/preview-image/lazy?platform=${platform}`"
      >
        <template v-slot:placeholder>
          <div class="d-flex align-center justify-center fill-height">
            <v-progress-circular
                :indeterminate="true"
                color="grey-lighten-4"
            ></v-progress-circular>
          </div>
        </template>
        <v-expand-transition>
          <div
            v-if="hover"
            class="d-flex transition-fast-in-fast-out black v-card--reveal text-h2"
            style="height: 100%;"
          >
            <v-btn
              variant="plain"
              :icon="true"
              size="70"
              :href="`https://asv-api.jomichaelis.de/api/v21/preview-image?team=${team}&platform=${platform}`"
              target="_blank"
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
export default {
  name: "MatchdayCard",
  props: {
    team: {
      type: Number,
      default: 1
    },
    platform: {
      type: String,
      default: 'facebook'
    },
  },
  data() {
    return {

    }
  },
  methods: {
    download() {
      this.$axios
        .$get(
          "https://asv-api.jomichaelis.de/api/v21/preview-image?team=" + this.team + "&platform=" + this.platform,
        )
        .then(response => console.log(response))
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