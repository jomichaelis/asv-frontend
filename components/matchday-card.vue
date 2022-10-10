<template>
  <v-hover v-slot="{ isHovering, props }">
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
              indeterminate="true"
              color="grey-lighten-4"
            ></v-progress-circular>
          </div>
        </template>
        <v-expand-transition>
          <div
            v-if="isHovering"
            class="d-flex transition-fast-in-fast-out bg-black v-card--reveal text-h2"
            style="height: 100%;"
          >
            <v-btn
              variant="plain"
              :icon="true"
              size="70"
              @click="download"
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
  data: () => ({
  }),
  methods: {
    async download() {
      await fetch("https://asv-api.jomichaelis.de/api/v21/preview-image?team=" + this.team + "&platform=" + this.platform, { method: 'get', mode: 'no-cors', referrerPolicy: 'no-referrer' })
        .then(res => res.blob())
        .then(res => {
          const aElement = document.createElement('a');
          aElement.setAttribute('download', "asv1.jpg");
          const href = URL.createObjectURL(res);
          aElement.href = href;
          aElement.setAttribute('target', '_blank');
          aElement.click();
          URL.revokeObjectURL(href);
        });
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