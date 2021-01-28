<template>
  <v-container class="align-start">
    <v-card>
      <v-card-title class="text-center justify-center py-6">
        <h1 class="font-weight-bold display-3 second--text">
          {{ Analysis.title }}
        </h1>
      </v-card-title>
      <v-card-subtitle class="text-center">
        <div>
          {{
            new Date(Analysis.starting_date).toLocaleDateString("en-en", {
              year: "numeric",
              month: "short",
              day: "numeric",
            })
          }}
        </div>
        <v-divider class="my-5"></v-divider>
        {{ Analysis.description }}
        <!-- If user can't edit this analysis show warning message -->

        <div v-if="!canUserEdit" class="red--text lighten-4">
          <v-icon class="red--text lighten-4">new_releases</v-icon>
          {{ closedAnalysisWarningMessage }}
        </div>
      </v-card-subtitle>

      <v-tabs v-model="currentTab" color="second" grow>
        <v-tab v-for="item in barItems" :key="item.id">
          {{ item.name }}
        </v-tab>
      </v-tabs>

      <v-tabs-items v-model="currentTab">
        <v-tab-item v-for="item in barItems" :key="item.id">
          <v-card flat>
            <v-card-text>
              <component :is="item.component_name"></component>
            </v-card-text>
          </v-card>
        </v-tab-item>
      </v-tabs-items>
    </v-card>
  </v-container>
</template>

<script>
// Here we use nuxt dynamic components
// Check: https://github.com/nuxt/components/issues/13

export default {
  // This route required authentication
  middleware: "authenticated",

  async asyncData({ params, redirect, $axios }) {
    let Analysis = null;
    try {
      Analysis = await $axios
        .get(`/swot_analyses/${params.id}/`)
        .then((res) => res.data);
    } catch (err) {
      // If error redirect to analysis dashboard
      redirect("/analysis");
    }
    return { Analysis };
  },
  data: () => ({
    currentTab: null,
    barItems: [
      {
        name: "Internal factors",
        component_name: "InternalFactorsTable",
      },
      {
        name: "External factors",
        component_name: "ExternalFactorsTable",
      },
      { name: "SWOT Matrix", component_name: "SWOTMatrix" },
      { name: "Graphs", component_name: "Graphs" },
    ],
    closedAnalysisWarningMessage:
      "Warning: This analysis is closed. If you wish to make any changes please reopen it.",
  }),
  computed: {
    // Check if user can edit the analysis
    canUserEdit() {
      return this.Analysis.state == "Open";
    },
  },
};
</script>
