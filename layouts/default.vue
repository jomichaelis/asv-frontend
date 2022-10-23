<template>
  <v-app id="inspire">
    <v-app-bar
        clipped-left
        fixed
        app
        color="#eee"
        elevation="0"
        height="80"
  >
      <v-container class="d-flex align-center">
        <v-avatar
            class="mr-10 ml-4 my-4"
            size="56"
            tile
        >
          <v-img
            src="/asv-logo200.png"
            alt="ASV Logo"
            contain
          />
        </v-avatar>

        <div class="d-none d-sm-flex">
          <v-btn
            class="mx-1"
            v-for="link in links"
            :key="link.name"
            text
            :to=link.link
          >
            {{ link.name }}
          </v-btn>
          <v-btn
              class="mx-1"
              text
              href="https://cloud.jomichaelis.de/s/cBKW5XRsn7CDpsb"
              target="_blank"
          >
            Fotos
            <v-icon
                right
                dark
                class="pl-2"
            >
              mdi-open-in-new
            </v-icon>
          </v-btn>
        </div>

        <v-spacer />

        <v-app-bar-nav-icon
            @click="drawer = !drawer"
            class="d-flex d-sm-none"
        ></v-app-bar-nav-icon>
      </v-container>
    </v-app-bar>

    <v-navigation-drawer
        v-model="drawer"
        absolute
        :temporary="true"
    >
      <v-list
          :nav="true"
          dense
      >
        <v-list-item
          v-for="(item, i) in links"
          :key="i"
          :to="item.link"
          router
          exact
          active-class="primary--text"
        >
          <v-list-item-title v-text="item.name" />
        </v-list-item>
        <v-list-item
            href="https://cloud.jomichaelis.de/s/cBKW5XRsn7CDpsb"
            active-class="primary--text"
            target="_blank"
        >
          <v-list-item-title>
            Fotos
          </v-list-item-title>
          <v-list-item-icon>
            <v-icon>
              mdi-open-in-new
            </v-icon>
          </v-list-item-icon>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main class="bg-grey-lighten-3">
      <v-container>
        <nuxt />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  data: () => ({
    drawer: false,
    links: [
      {
        name: 'Dashboard',
        link: '/'
      },
      {
        name: 'Matchday',
        link: '/matchday'
      },
    ],
  }),
  created() {
    this.$store.dispatch("bindMatchdayImages")
  }
}
</script>
