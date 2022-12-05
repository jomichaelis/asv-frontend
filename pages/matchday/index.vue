<template>
  <v-container>
    <h2>Matchday Images</h2>
    <v-expansion-panels
      class="my-4"
      multiple
      v-model="panels"
    >
      <v-expansion-panel
        v-for="(item,i) in 2"
        :key="`team_${i}`"
      >
        <v-expansion-panel-header>
          <h3>
            ASV {{i + 1}}
          </h3>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-row>
            <v-col
              v-for="(k,j) in imagesFilteredByTeam(i+1)"
              :key="`team_${i}_img_${j}`"
              :cols="k['platform'] === 'facebook' ? 12 : 6"
              :sm="k['platform'] === 'facebook' ? 6 : 3"
            >
              <MatchdayCard :imageURL="k['imageURL']" :platform="k['platform']" :team=i+1 :loading="k['loading']" />
            </v-col>
          </v-row>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
    <v-row class="justify-center my-8">
      <v-btn @click="regenerateImages" outlined :loading="buttonLoading">
        regenerate
      </v-btn>
    </v-row>
  </v-container>
</template>

<script>
import MatchdayCard from "../../components/matchday-card";
import axios from "axios";
export default {
  data() {
    return {
      panels: [0, 1],
      buttonLoading: false
    }
  },
  components: {
    MatchdayCard
  },
  computed: {
    images() {
      return this.$store.getters.all
    }
  },
  methods: {
    imagesFilteredByTeam(team) {
      return this.images.filter((doc) => {
        return doc.team === team
      })
    },
    async regenerateImages() {
      this.buttonLoading = true
      await this.$axios.$get('https://asv-matchday-preview-generator-public-ynj2djdt3a-lm.a.run.app?platform=facebook&team=1')
      await this.$axios.$get('https://asv-matchday-preview-generator-public-ynj2djdt3a-lm.a.run.app?platform=instagram&team=1')
      await this.$axios.$get('https://asv-matchday-preview-generator-public-ynj2djdt3a-lm.a.run.app?platform=facebook&team=2')
      await this.$axios.$get('https://asv-matchday-preview-generator-public-ynj2djdt3a-lm.a.run.app?platform=instagram&team=2')
      this.buttonLoading = false
    }
  }
}
</script>
