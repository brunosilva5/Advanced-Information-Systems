<template>
  <!-- Wait for fetch to render -->
  <v-card v-if="!$fetchState.pending" flat tile>
    <v-row>
      <v-col cols="4">
        <v-card-title class="justify-center"
          >Your global evaluation
        </v-card-title>
        <v-card-text class="text-center">
          <v-progress-circular
            :size="150"
            :width="15"
            :value="score"
            color="second"
          >
            <h2>{{ score }}</h2>
          </v-progress-circular>
        </v-card-text>
      </v-col>
      <v-col cols="8" class="forth">
        <h2 class="font-weight-medium ma-16 pa-16">
          {{ getMessage() }}
        </h2>
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
  computed: {
    score() {
      return this.getScore();
    },
  },
  methods: {
    getQuadrant(name) {
      return this.quadrants.filter((item) => item.q_type == name)[0];
    },
    // Compute a global score, according to formula:
    // Score=((S/S+W) + (O/O+T)) * 50
    // Where Scores takes a range 0-100
    getScore() {
      const S = this.getQuadrant("Strengths").total_score;
      const W = this.getQuadrant("Weaknesses").total_score;
      const O = this.getQuadrant("Opportunities").total_score;
      const T = this.getQuadrant("Threats").total_score;

      const SW = S + W;
      const OT = O + T;

      let score = S / SW;
      score += O / OT;
      score *= 50;
      return parseFloat(score).toFixed(2);
    },
    getMessage() {
      if (this.score < 20) {
        return "Your business seems to be performing very poorly!";
      } else if (this.score < 40) {
        return "Your business seems to be performing poorly!";
      } else if (this.score < 60) {
        return "Your business seems to be going in the right path, don't settle.";
      } else if (this.score < 80) {
        return "Your business seems to be performing good!";
      } else {
        return "Your business seems to be excelent! Good job!";
      }
    },
  },
};
</script>
