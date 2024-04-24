<template>
  <div>
    <v-app v-if="!loading">
      <v-app-bar elevation="0" color="navbar">
        <v-app-bar-nav-icon
          v-if="mobileNavigation"
          @click="drawer = !drawer"
        >
        </v-app-bar-nav-icon>

        <router-link :to="{ name: 'Home' }" style="width: 50px;">
          <v-img
            :class="mobileNavigation ? 'ml-2' : 'ml-4'"
            src="@/assets/asv-logo200.png"
            height="42"
            width="42"
            contain
          />
        </router-link>

        <router-link :to="{ name: 'Home' }" class="title-link appbar-title ml-3 mt-1">
          <span class="title ml-3 mr-5 white--text">asv<span class="font-weight-light">.webservices</span></span>
        </router-link>
      </v-app-bar>

      <div :class="mobileNavigation ? 'nav-drawer-mobile' : 'nav-drawer'">
        <v-navigation-drawer
          v-model="drawer"
          :expand-on-hover="!mobileNavigation"
          :rail="!mobileNavigation"
          color="navbar"
        >
          <v-list nav :lines="false">
            <template v-for="item in navProperties" :key="item.title">
              <v-list-item
                v-if="item.to"
                :title="item.title"
                :prepend-icon="item.icon"
                :to="{ name: item.to }"
                :value="item.title"
                color="primary"
              ></v-list-item>
              <v-list-item
                v-else-if="item.href"
                :title="item.title"
                :prepend-icon="item.icon"
                :href="item.href"
                :value="item.title"
                target="_blank"
                color="primary"
              ></v-list-item>
            </template>
          </v-list>

          <template v-slot:append>
            <!--
            <v-list nav :lines="false">
              <v-list-item
                title="Einstellungen"
                prepend-icon="mdi-cog"
                color="primary"
              ></v-list-item>
            </v-list>
            -->
            <v-divider />
            <v-list-item lines="two">
              <template v-slot:prepend>
                <Avatar :userID="authStore?.uid" />
              </template>
              <v-list-item-title v-text="authStore?.displayName" class="ml-1" />
              <v-list-item-subtitle v-text="authStore?.email" class="ml-1" />
              <template v-slot:append>
                <v-tooltip text="Abmelden">
                  <template v-slot:activator="{ props }">
                    <v-btn v-bind="props" icon="mdi-logout" variant="text" color="primary" @click="onSignOut"/>
                  </template>
                </v-tooltip>
              </template>
            </v-list-item>
          </template>
        </v-navigation-drawer>
      </div>

      <v-main>
        <router-view />
      </v-main>
      <!--
      <v-footer style="background-color: var(--v-theme-background); border-top: 1px solid #AAA; max-height: 50px;">
        <v-row justify="center" no-gutters>
          <v-col class="my-3" cols="auto">
            {{ new Date().getFullYear() }} — <strong>Stamm Silberfüchse</strong>
          </v-col>
        </v-row>
      </v-footer>
      -->
    </v-app>
    <v-app v-else>
      <v-main>
        <v-container class="fill-height">
          <v-responsive class="align-center text-center fill-height mx-2">
            <div class="main-div">
              <v-row justify="center">
                <v-col cols="6">
                  <v-progress-linear
                    color="primary"
                    indeterminate
                    rounded
                    height="6"
                    style="max-width: 150px;"
                  />
                </v-col>
              </v-row>
            </div>
          </v-responsive>
        </v-container>
      </v-main>
    </v-app>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { useTheme } from 'vuetify'
import { signOut } from '@/plugins/firebase'

import { useAuthStore } from '@/store/auth'
import { useTeamsStore } from '@/store/teams'
import { useUpcomingMatchesStore } from '@/store/upcomingMatches'
import { useMatchdayPreviewsStore } from '@/store/matchdayPreviews'

import Avatar from '@/components/Avatar.vue'

const router = useRouter()

const authStore = useAuthStore()
const teamsStore = useTeamsStore()
const upcomingMatchesStore = useUpcomingMatchesStore()
const matchdayPreviewsStore = useMatchdayPreviewsStore()

const drawer = ref(true)

const displayWidth = ref(1920)

const loading = ref(true)

onMounted(async () => {
  loading.value = true

  // navbar
  window.addEventListener('resize', onResize, { passive: true })
  onResize()

  // load Stores
  await teamsStore.bind()
  await upcomingMatchesStore.bind()
  await matchdayPreviewsStore.bind()

  loading.value = false
})

const onSignOut = () => {
  signOut()
    .then(() => {
      router.push({ name: 'Anmelden' })
    })
}

const onResize = () => {
  displayWidth.value = window.innerWidth
  if(window.innerWidth < 1280) {
    drawer.value = false
  } else {
    drawer.value = true
  }
}

const mobileNavigation = computed(() => {
  return displayWidth.value < 1280
})

onBeforeUnmount(() => {
  if (typeof window === 'undefined') return
  window.removeEventListener('resize', onResize, { passive: true })
})

</script>

<script>
export default {
  data: () => ({
    drawer: true,
    navProperties: [
      {
        title: 'Start',
        icon: 'mdi-home',
        to: 'Home'
      },
      {
        title: 'Matchday',
        icon: 'mdi-image-multiple',
        to: 'Matchday'
      },
      {
        title: 'Fotos',
        icon: 'mdi-open-in-new',
        href: 'https://cloud.jomichaelis.de/s/nY93bJXrmCmzTDz'
      },
      {
        title: 'Verwaltung',
        icon: 'mdi-cog-outline',
        to: 'Verwaltung'
      },
    ]
  }),
}
</script>

<style lang="scss">
@import url('https://fonts.googleapis.com/css2?family=Borel&display=swap');

.appbar-title {
  font-size: 24px !important;
}

.title-link, .title-link:link, .title-link:visited, .title-link:hover, .title-link:active {
  cursor: pointer;
  text-decoration: none;
  color: var(--v-theme-on-surface);
}

.nav-drawer > nav > div > div > div > .v-list-group > .v-list-group__items .v-list-item {
  transition: all 0.2s;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  padding-inline-start: 8px !important;
}

.nav-drawer > nav.v-navigation-drawer--is-hovering > div > div > div > .v-list-group > .v-list-group__items > a {
  padding-inline-start: 20px !important;
}

.nav-drawer-mobile > nav > div > div > div > .v-list-group > .v-list-group__items .v-list-item {
  padding-inline-start: 20px !important;
}

.v-navigation-drawer--is-hovering .sublist-mobile > div > div > div > div > .v-list-group__items > a {
  padding-inline-start: 20px !important;
}

.v-navigation-drawer--rail:not(.v-navigation-drawer--is-hovering.v-navigation-drawer--expand-on-hover) .v-avatar.v-avatar--size-default {
  --v-avatar-height: 24px !important;
}
.v-navigation-drawer--rail:not(.v-navigation-drawer--is-hovering.v-navigation-drawer--expand-on-hover) .v-list-item__append {
  visibility: hidden;
}
</style>
