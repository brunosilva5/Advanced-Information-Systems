<template>
  <BaseFactorsTable
    :possible-classifications="possibleClassifications"
    :factors="factors"
  />
</template>
<script>
import BaseFactorsTable from "~/components/BaseFactorsTable";
export default {
  components: { BaseFactorsTable },
  data: () => ({
    quadrants: ["Strengths", "Weaknesses"],
    // List of factors
    factors: [],
    // Possible options for factor classification form
    possibleClassifications: [],
  }),
  async fetch() {
    // Fetch the internal quadrants of the current analysis
    let quadrants = await this.$axios
      .get(`/swot_analyses/${this.analysisId}/`)
      .then((res) => res.data.quadrants);

    let strengths_quadrant = quadrants.filter(function (q) {
      return q.q_type == "Strengths";
    })[0];

    // Create object for possible classifications
    this.possibleClassifications.push({
      text: "Strength",
      value: 0,
      quadrant_id: strengths_quadrant.id,
    });

    // Now we search for the second quadrant
    let weaknesses_quadrant = quadrants.filter(function (q) {
      return q.q_type == "Weaknesses";
    })[0];

    // Create object for possible classifications
    this.possibleClassifications.push({
      text: "Weakness",
      value: 1,
      quadrant_id: weaknesses_quadrant.id,
    });

    // Now we join the factors from both quadrants
    this.factors = [
      ...strengths_quadrant.factors,
      ...weaknesses_quadrant.factors,
    ];
  },
  computed: {
    // Get analysis id from url
    analysisId() {
      return this.$route.params.id;
    },
  },
};
</script>
