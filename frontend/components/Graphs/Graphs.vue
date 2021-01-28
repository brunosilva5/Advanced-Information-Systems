<template>
  <v-container>
    <v-row align="center" justify="center">
      <v-col v-for="item in displayGraphs" :key="item.id" cols="12" md="5">
        <v-card height="400">
          <v-responsive :aspect-ratio="4 / 3">
            <v-card-text class="text-center" style="word-break: normal">
              <h1 class="h1 pa-5 third--text">{{ item.title }}</h1>
              <component :is="item.component_name" v-bind="props"></component>
            </v-card-text>
          </v-responsive>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data: () => ({
    series: [],

    displayGraphs: [
      {
        title: "General analysis of internal and external factors",
        component_name: "PolarArea",
      },
      { title: "Radar graph", component_name: "Radar" },
    ],
  }),
  async fetch() {
    // Get the quadrants of an analysis
    let quadrants = await this.$axios
      .get(`/swot_analyses/${this.$route.params.id}/quadrants/`)
      .then((res) => res.data);
    this.series = quadrants.map((q) => q.total_score);
  },
  computed: {
    analysisId() {
      return this.$route.params.id;
    },
    props() {
      return { series: this.series };
    },
  },
};
</script>

<style></style>
