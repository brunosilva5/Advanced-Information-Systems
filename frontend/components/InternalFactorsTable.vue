<template>
  <v-data-table :headers="headers" :items="factors" class="elevation-1">
    <template #top>
      <v-toolbar flat>
        <v-toolbar-title>Create Factor</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <FactorForm />
      </v-toolbar>
    </template>
  </v-data-table>
</template>
<script>
import FactorForm from "~/components/FactorForm";
export default {
  components: { FactorForm },
  // Id of analysis is passed in
  // eslint-disable-next-line vue/require-prop-types
  props: ["id"],
  data: () => ({
    headers: [
      { text: "Description", value: "description" },
      { text: "Classification", value: "Classification" },
      { text: "Importance", value: "importance" },
      { text: "Score", value: "score" },
    ],
    factors: [],
  }),
  async fetch() {
    // Fetch the quadrants of the current analysis
    let quadrants = await this.$axios
      .get(`/swot_analyses/${this.id}/`)
      .then((res) => res.data.quadrants);

    // Now we filter for the "Strenghts" and "Weaknesses" quadrants
    quadrants = quadrants.filter(function (q) {
      return q.q_type == "Strengths" || q.q_type == "Weaknesses";
    });

    // Now we join the factors from both quadrants
    this.factors = [...quadrants[0].factors, ...quadrants[1].factors];
  },
};
</script>
