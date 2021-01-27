<template>
  <v-data-table :headers="headers" :items="factors" class="elevation-1">
    <template #top>
      <v-toolbar flat>
        <v-toolbar-title>Create Factor</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <!-- Wait until fetch has finished -->
        <div v-if="!$fetchState.pending">
          <FactorForm
            :quadrant1="quadrant_1"
            :quadrant2="quadrant_2"
            :analysis-id="id"
          />
        </div>
      </v-toolbar>
    </template>
  </v-data-table>
</template>
<script>
import FactorForm from "~/components/FactorForm";
export default {
  components: { FactorForm },
  props: {
    // Id of analysis is passed in
    id: {
      type: Number,
      required: true,
    },
    // `q_type` of quadrant 1
    quadrant1Qtype: {
      type: String,
      required: true,
    },
    // `q_type` of quadrant 2
    quadrant2Qtype: {
      type: String,
      required: true,
    },
  },
  data: () => ({
    headers: [
      { text: "Description", value: "description" },
      { text: "Classification", value: "Classification" },
      { text: "Importance", value: "importance" },
      { text: "Score", value: "score" },
    ],
    factors: [],
    // Save the first quadrant
    quadrant_1: null,
    // Save the second quadrant
    quadrant_2: null,
  }),
  async fetch() {
    // Fetch the quadrants of the current analysis
    let quadrants = await this.$axios
      .get(`/swot_analyses/${this.id}/`)
      .then((res) => res.data.quadrants);

    // Now we search for the first quadrant
    let search_type = this.quadrant1Qtype;
    let quadrant_1 = quadrants.filter(function (q) {
      return q.q_type == search_type;
    })[0];
    // Save quadrant 1
    this.quadrant_1 = { name: this.quadrant1Qtype, id: quadrant_1.id };

    // Now we search for the second quadrant
    search_type = this.quadrant2Qtype;
    let quadrant_2 = quadrants.filter(function (q) {
      return q.q_type == search_type;
    })[0];

    // Save quadrant 2
    this.quadrant_2 = { name: this.quadrant2Qtype, id: quadrant_2.id };

    // Now we join the factors from both quadrants
    this.factors = [...quadrant_1.factors, ...quadrant_2.factors];
  },
};
</script>
