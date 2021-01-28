<template>
  <!-- Wait for fetch to render -->
  <v-card v-if="!$fetchState.pending" flat tile>
    <v-row v-for="item in quadrants" :key="item.id" class="py-2">
      <v-col cols="2" class="second white--text">
        {{ item.q_type }}
      </v-col>
      <v-col cols="2" class="third white--text">
        <v-card
          flat
          tile
          class="text-center white--text third align-center justify-center"
          height="100%"
        >
          {{ item.total_score }}
        </v-card>
      </v-col>
      <v-col cols="8" class="forth">
        {{ getMessage(item) }}
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
export default {
  data: () => ({
    quadrants: [],
  }),
  async fetch() {
    // Get the quadrants of an analysis
    this.quadrants = await this.$axios
      .get(`/swot_analyses/${this.$route.params.id}/quadrants/`)
      .then((res) => res.data);
  },
  methods: {
    getMessage(item) {
      if (item.q_type === "Strengths") {
        const weaknesses = this.quadrants.filter(
          (item) => item.q_type == "Weaknesses"
        )[0];
        if (item.total_score < weaknesses.total_score) {
          return "Your strengths are lower than your weaknesses, that's not a good sign.";
        }
        return "Your strengths are greater than your weaknesses, that' a good sign.";
      }

      if (item.q_type === "Weaknesses") {
        const strengths = this.quadrants.filter(
          (item) => item.q_type == "Strengths"
        )[0];
        if (item.total_score < strengths.total_score) {
          return "Your weaknesses are lower than your strengths, that's a good sign.";
        }
        return "Your weaknesses are greater than your strengths, that's not a good sign.";
      }

      if (item.q_type === "Opportunities") {
        const threats = this.quadrants.filter(
          (item) => item.q_type == "Threats"
        )[0];
        if (item.total_score < threats.total_score) {
          return "Your opportunities are lower than your threats, that's not a good sign.";
        }
        return "Your opportunities are greater than your threats, that's a good sign.";
      }

      if (item.q_type === "Threats") {
        const opportunities = this.quadrants.filter(
          (item) => item.q_type == "Opportunities"
        )[0];
        if (item.total_score < opportunities.total_score) {
          return "Your threats are lower than your opportunities, that's a good sign.";
        }
        return "Your threats are greater than your opportunities, that's not a good sign.";
      }
    },
  },
};
</script>
