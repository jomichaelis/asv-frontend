<template>
  <v-container>
    <h2>Matchday Images</h2>
    <v-row class="mt-2">
      <v-col
          cols="12"
          sm="6"
      >
        <MatchdayCard platform="facebook" team="1" />
      </v-col>
      <v-col
          cols="12"
          sm="6"
      >
        <MatchdayCard platform="facebook" team="2" />
      </v-col>
    </v-row>
    <v-row class="mt-2">
      <v-col
          cols="12"
          sm="3"
      >
        <MatchdayCard platform="instagram" team="1" />
      </v-col>
      <v-col
          cols="12"
          sm="3"
      >
        <MatchdayCard platform="instagram" team="2" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import MatchdayCard from "../../components/matchday-card";
export default {
  data: () => ({
  }),
  components: {
    MatchdayCard
  }
}
</script>