<template>
  <div v-if="!$fetchState.pending">
    <v-row>
      <!-- Strengths -->
      <v-col cols="12">
        <GlobalScore />
      </v-col>
    </v-row>
    <v-row class="pt-5">
      <v-col cols="12"><GlobalFactorsAnalyse /></v-col>
    </v-row>
  </div>
</template>

<script>
import GlobalScore from "~/components/Recommendations/GlobalScore";
import GlobalFactorsAnalyse from "~/components/Recommendations/GlobalFactorsAnalyse";

export default {
  components: { GlobalScore, GlobalFactorsAnalyse },
  async fetch() {
    // Get the quadrants of an analysis
    this.quadrants = await this.$axios
      .get(`/swot_analyses/${this.$route.params.id}/quadrants/`)
      .then((res) => res.data);
  },
};
</script>
