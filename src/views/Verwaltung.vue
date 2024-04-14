<template>
  <v-container class="fill-height">
    <v-responsive class="fill-height">
      <div class="main-div">
        <PageTitle title="Verwaltung" />

        <div class="mx-3 mt-3 mb-4">
          <v-row>
            <v-col cols="12">
              <v-tabs
                v-model="tab"
                bg-color="grey-darken-4"
                grow
                color="primary"
              >
                <v-tab
                  v-for="item in tabs"
                  :key="item.key"
                  :value="item.key"
                  class="text-none"
                >
                  {{ item.text }}
                </v-tab>
              </v-tabs>

              <v-window v-model="tab" :touch="false">
                <v-window-item key="teams" value="teams">
                  <Teams />
                </v-window-item>
                <v-window-item key="asv-teams" value="asv-teams">
                  <Teams :asv-only="true" />
                </v-window-item>
                <v-window-item key="settings" value="settings">
                  <v-card class="mt-10">
                    <v-card-title>
                      Einstellungen
                    </v-card-title>
                  </v-card>
                </v-window-item>
              </v-window>
            </v-col>
          </v-row>
        </div>
      </div>
    </v-responsive>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue'

import PageTitle from '@/components/PageTitle.vue'
import Teams from '@/components/verwaltung/teams/Teams.vue'

const tabs = ref([
  { key: 'teams', text: 'Teams' },
  { key: 'asv-teams', text: 'ASV-Teams'},
  { key: 'settings', text: 'Einstellungen'}
])

const tab = ref(tabs.value[0].key)

</script>
