<template>
  <apexchart
    type="polarArea"
    :options="chartOptions"
    :series="series"
  ></apexchart>
</template>
<script>
import ApexCharts from "vue-apexcharts";

export default {
  components: { apexchart: ApexCharts },
  data: () => ({
    series: [],
    chartOptions: {
      chart: {
        type: "polarArea",
        toolbar: { show: true },
      },
      labels: ["Strengths", "Weaknesses", "Opportunities", "Threats"],
    },
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
  },
};
</script>
