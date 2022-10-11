<template>
  <v-container>
    <h2>Matchday Images</h2>
    <v-row class="mt-2">
      <v-col
          cols="12"
          sm="6"
      >
        <MatchdayCard platform="facebook" :team="1" />
      </v-col>
      <v-col
          cols="12"
          sm="6"
      >
        <MatchdayCard platform="facebook" :team="2" />
      </v-col>
    </v-row>
    <v-row class="mt-2">
      <v-col
          cols="12"
          sm="3"
      >
        <MatchdayCard platform="instagram" :team="1" />
      </v-col>
      <v-col
          cols="12"
          sm="3"
      >
        <MatchdayCard platform="instagram" :team="2" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import MatchdayCard from "../../components/matchday-card";
import axios from "axios";
export default {
  data() {
    return {

    }
  },
  components: {
    MatchdayCard
  },
  methods: {
    getBase64(url) {
      return axios
        .get(url, {
          responseType: 'arraybuffer'
        })
        .then(response => new Buffer(response.data, 'binary').toString('base64'))
      }
  }
}
</script>