<template>
  <!-- Until until fetch is finished to render -->
  <div v-if="!$fetchState.pending">
    <v-row>
      <!-- Strengths -->
      <v-col cols="12" md="6">
        <SmallTable :quadrant="strengthsQuadrant" color="green" />
      </v-col>
      <v-col cols="12" md="6">
        <SmallTable :quadrant="weaknessesQuadrant" color="red" />
      </v-col>
    </v-row>
    <v-row>
      <!-- Strengths -->
      <v-col cols="12" md="6">
        <SmallTable :quadrant="opportunitiesQuadrant" color="green" />
      </v-col>
      <v-col cols="12" md="6">
        <SmallTable :quadrant="threatsQuadrant" color="red" />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import SmallTable from "~/components/SmallTable";
export default {
  components: {
    SmallTable,
  },
  data: () => ({
    quadrants: [],
  }),
  async fetch() {
    // Get the quadrants of an analysis
    this.quadrants = await this.$axios
      .get(`/swot_analyses/${this.$route.params.id}/quadrants/`)
      .then((res) => res.data);
  },

  computed: {
    strengthsQuadrant() {
      return this.getQuadrant("Strengths");
    },
    weaknessesQuadrant() {
      return this.getQuadrant("Weaknesses");
    },
    opportunitiesQuadrant() {
      return this.getQuadrant("Opportunities");
    },
    threatsQuadrant() {
      return this.getQuadrant("Threats");
    },
  },
  methods: {
    // Returns a quadrant by name
    getQuadrant(name) {
      const factors = this.quadrants
        .filter((item) => item.q_type === name)[0]
        .factors.sort(function (a, b) {
          return b.score - a.score;
        });
      const score = this.quadrants.filter((item) => item.q_type === name)[0]
        .total_score;

      return { title: name, factors: factors, total_score: score };
    },
  },
};
</script>
