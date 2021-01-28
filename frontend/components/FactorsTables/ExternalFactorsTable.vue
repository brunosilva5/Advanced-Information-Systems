<template>
  <BaseFactorsTable
    :possible-classifications="possibleClassifications"
    :factors="factors"
  />
</template>
<script>
import BaseFactorsTable from "~/components/FactorsTables/BaseFactorsTable";
export default {
  components: { BaseFactorsTable },
  data: () => ({
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

    let opportunities_quadrant = quadrants.filter(function (q) {
      return q.q_type == "Opportunities";
    })[0];

    // Create object for possible classifications
    this.possibleClassifications.push({
      text: "Opportunity",
      value: 3,
      quadrant_id: opportunities_quadrant.id,
    });

    // Now we search for the second quadrant
    let threats_quadrant = quadrants.filter(function (q) {
      return q.q_type == "Threats";
    })[0];

    // Create object for possible classifications
    this.possibleClassifications.push({
      text: "Threat",
      value: 2,
      quadrant_id: threats_quadrant.id,
    });

    // Now we join the factors from both quadrants
    this.factors = [
      ...opportunities_quadrant.factors,
      ...threats_quadrant.factors,
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
