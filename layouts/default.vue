<template>
  <v-app id="inspire">
    <v-app-bar flat height="72">
      <v-container class="fill-height d-flex align-center">
        <v-avatar
            class="mr-10 ml-4 my-4"
            size="56"
            image="asv-logo.png"
        >
        </v-avatar>

        <div class="d-none d-sm-flex">
          <v-btn
              class="mx-1"
              v-for="link in links"
              :key="link"
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

        <v-spacer></v-spacer>

        <v-app-bar-nav-icon
          @click="drawer = !drawer"
          class="d-flex d-sm-none"
        ></v-app-bar-nav-icon>
      </v-container>
    </v-app-bar>

    <v-navigation-drawer
      v-model="drawer"
      absolute
      temporary="true"
    >
      <v-list
        nav="true"
        dense
      >
        <v-list-item
            v-for="item in links"
            :key="item.name"
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
            <v-icon
                right
                dark
                class="pl-2"
            >
              mdi-open-in-new
            </v-icon>
          </v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main class="bg-grey-lighten-3">
      <v-container>
        <v-row>
          <!--
          <v-col cols="2">
            <v-sheet rounded="lg">
              <v-list rounded="lg">
                <v-list-item
                    v-for="n in 5"
                    :key="n"
                    link
                >
                  <v-list-item-title>
                    List Item {{ n }}
                  </v-list-item-title>
                </v-list-item>

                <v-divider class="my-2"></v-divider>

                <v-list-item
                    link
                    color="grey-lighten-4"
                >
                  <v-list-item-title>
                    Refresh
                  </v-list-item-title>
                </v-list-item>
              </v-list>
            </v-sheet>
          </v-col>
          -->

          <v-col>
            <v-sheet
                min-height="70vh"
                rounded="lg"
                class="pa-3"
            >
              <slot />
            </v-sheet>
          </v-col>
        </v-row>
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
}
</script>
