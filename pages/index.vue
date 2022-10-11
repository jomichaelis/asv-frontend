<template>
  <v-container>
    <h2>Dashboard</h2>
    <img :src="`data:image/png;base64,${this.imageData}`" alt="test" />
  </v-container>
</template>

<script>

export default {
  async fetch() {
    const vm = this
    this.$axios
      .get("https://asv-api.jomichaelis.de/api/v21/preview-image/")
      .then(function(response) {
        console.log(response)
        console.log(new Buffer(response.data, 'binary').toString('base64'))
        console.log(vm)
        vm.imageData = new Buffer(response.data, 'binary').toString('base64')
      })
    // .then(response => console.log(response))
  },
  data() {
    return {
      imageData: 'abc'
    }
  },
}
</script>