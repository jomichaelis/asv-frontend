<template>
  <v-container class="fill-height">
    <v-responsive class="fill-height">
      <div class="main-div">
        <PageTitle title="Verwaltung" />

        <div class="mx-3 mt-3 mb-4">
          <v-row>
            <v-col cols="12" md="6" lg="4">
              <v-card class="pa-0">
                <v-card-text class="mb-6 py-3">
                  <v-card-title class="text-h5 text--primary mb-5 pr-1 pl-2">
                    <v-row class="mx-0 mt-0 pb-2">
                      Teams
                    </v-row>
                  </v-card-title>
                  <div class="ml-3 mr-1 content">
                    <v-virtual-scroll
                      :height="300"
                      :items="teams"
                    >
                      <template v-slot:default="{ item }">
                        <v-list-item>
                          <template v-slot:prepend>
                            <v-avatar
                              :color="item.color"
                              class="text-white"
                              size="40"
                            >
                              {{ item.initials }}
                            </v-avatar>
                          </template>

                          <v-list-item-title>{{ item.fullName }}</v-list-item-title>

                          <template v-slot:append>
                            <v-btn
                              size="small"
                              variant="tonal"
                            >
                              View User

                              <v-icon
                                color="orange-darken-4"
                                end
                              >
                                mdi-open-in-new
                              </v-icon>
                            </v-btn>
                          </template>
                        </v-list-item>
                      </template>
                    </v-virtual-scroll>
                  </div>

                  <v-row justify="center">
                    <v-btn
                      prepend-icon="mdi-plus"
                      size="small"
                      border
                      variant="text"
                      class="text-none mt-3"
                    >
                      Hinzufügen
                    </v-btn>
                  </v-row>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </div>
      </div>
    </v-responsive>
  </v-container>
</template>

<script setup>
import PageTitle from '@/components/PageTitle.vue'

</script>
