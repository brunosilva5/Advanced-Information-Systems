<template>
  <v-container class="align-start">
    <v-card>
      <v-card-title class="text-center justify-center py-6">
        <h1 class="font-weight-bold display-3 second--text">
          {{ Analysis.title }}
        </h1>
      </v-card-title>
      <v-card-subtitle class="text-center">
        {{ Analysis.description }}
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
              <component :is="item.component_name" v-bind="Props"></component>
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
        component_name: "FactorsTable",
      },
      {
        name: "External factors",
        component_location: "ExternalFactorsTable",
      },
      { name: "SWOT Matrix" },
      { name: "Data crossing" },
      { name: "Graphs" },
    ],
  }),
  computed: {
    Props: function () {
      let props = null;
      // If internal table
      if (this.currentTab === 0) {
        props = {
          id: this.Analysis.id,
          quadrant1Qtype: "Strengths",
          quadrant2Qtype: "Weaknesses",
        };
      }
      return props;
    },
  },
};
</script>
