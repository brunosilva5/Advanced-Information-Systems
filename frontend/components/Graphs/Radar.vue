<template>
  <apexchart
    type="radar"
    height="330"
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
        height: 350,
        type: "radar",
      },
      plotOptions: {
        radar: {
          size: 140,
          polygons: {
            strokeColors: "#bbe1fa",
          },
        },
      },
      colors: ["#3282b8"],
      markers: {
        size: 4,
        colors: ["#fff"],
        strokeColor: "#0f4c75",
        strokeWidth: 2,
      },

      xaxis: {
        categories: ["Strengths", "Weaknesses", "Opportunities", "Threats"],
        labels: {
          style: { colors: ["#1b262c"] },
        },
      },
    },
  }),
  async fetch() {
    // Get the quadrants of an analysis
    let quadrants = await this.$axios
      .get(`/swot_analyses/${this.$route.params.id}/quadrants/`)
      .then((res) => res.data);
    this.series = [
      { name: "Score", data: quadrants.map((q) => q.total_score) },
    ];
  },
  computed: {
    analysisId() {
      return this.$route.params.id;
    },
  },
};
</script>
