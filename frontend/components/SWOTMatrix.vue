<template>
  <!-- Until until fetch is finished to render -->
  <div v-if="!$fetchState.pending">
    <v-row>
      <!-- Strengths -->
      <v-col cols="12" md="6">
        <SWOTMatrixTable
          title="Strengths"
          :factors="getQuadrantFactors('Strengths')"
          :total-score="getQuadrantTotalScore('Strengths')"
          color="green"
        />
      </v-col>
      <v-col cols="12" md="6">
        <SWOTMatrixTable
          title="Weaknesses"
          :factors="getQuadrantFactors('Weaknesses')"
          :total-score="getQuadrantTotalScore('Weaknesses')"
          color="red"
        />
      </v-col>
    </v-row>
    <v-row>
      <!-- Strengths -->
      <v-col cols="12" md="6">
        <SWOTMatrixTable
          title="Opportunities"
          :factors="getQuadrantFactors('Opportunities')"
          :total-score="getQuadrantTotalScore('Opportunities')"
          color="green"
        />
      </v-col>
      <v-col cols="12" md="6">
        <SWOTMatrixTable
          title="Threats"
          :factors="getQuadrantFactors('Threats')"
          :total-score="getQuadrantTotalScore('Threats')"
          color="red"
        />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import SWOTMatrixTable from "~/components/SWOTMatrixTable";
export default {
  components: {
    SWOTMatrixTable,
  },
  data: () => ({
    quadrants: [],
  }),
  async fetch() {
    // Get the quadrants of an analysis
    this.quadrants = await this.$axios
      .get(`/swot_analyses/${this.analysisId}/quadrants/`)
      .then((res) => res.data);
  },
  computed: {
    // Get analysis id from url
    analysisId() {
      return this.$route.params.id;
    },
  },
  methods: {
    // Returns a quadrant by name
    getQuadrantFactors(name) {
      return this.quadrants
        .filter((item) => item.q_type === name)[0]
        .factors.sort(function (a, b) {
          return b.score - a.score;
        });
    },
    getQuadrantTotalScore(name) {
      return this.quadrants.filter((item) => item.q_type === name)[0]
        .total_score;
    },
  },
};
</script>

<style></style>
