<template>
  <ValidationObserver ref="observer" v-slot="{ invalid }">
    <v-form ref="form" @submit.prevent="createFactor">
      <v-row>
        <!-- Factor description -->
        <v-col cols="12" md="3">
          <ValidationProvider
            v-slot="{ errors }"
            vid="description"
            name="Description"
            rules="required"
          >
            <v-text-field
              v-model="factor.description"
              :error-messages="errors"
              counter="50"
              label="Description"
              maxlength="50"
            ></v-text-field>
          </ValidationProvider>
        </v-col>
        <!-- |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| -->
        <!-- Importance -->
        <v-col cols="12" md="3">
          <ValidationProvider
            v-slot="{ errors }"
            vid="importance"
            name="Importance"
            rules="required"
          >
            <v-text-field
              v-model="factor.importance"
              :error-messages="errors"
              label="Importance"
            ></v-text-field>
          </ValidationProvider>
        </v-col>
        <!-- |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| -->
        <!-- Classification -->
        <v-col cols="12" md="3">
          <ValidationProvider
            v-slot="{ errors }"
            vid="classification"
            name="Classification"
            rules="required"
          >
            <v-select
              v-model="factor.classification"
              item-text="text"
              item-value="value"
              :items="possibleClassifications"
              :error-messages="errors"
              label="Classification"
            ></v-select>
          </ValidationProvider>
        </v-col>

        <v-col cols="12" md="3">
          <v-btn
            depressed
            color="third"
            class="white--text"
            type="submit"
            :disabled="invalid"
          >
            Create factor
          </v-btn>
        </v-col>
      </v-row>
    </v-form>
  </ValidationObserver>
</template>
<script>
import { ValidationProvider, ValidationObserver } from "vee-validate";

export default {
  components: {
    ValidationProvider,
    ValidationObserver,
  },
  props: {
    // The id of analysis, required for POST
    analysisId: {
      type: Number,
      required: true,
    },
    // quadrant 1
    quadrant1: {
      type: Object,
      required: true,
    },
    // quadrant 2
    quadrant2: {
      type: Object,
      required: true,
    },
  },

  data: () => ({
    valid: false,
    factor: {
      description: null,
      importance: null,
      classification: 0,
    },
    // Lists all the possible classifications of a factor
    AllClassifications: [
      { text: "Strength", value: 0 },
      { text: "Weakness", value: 1 },
      { text: "Threat", value: 2 },
      { text: "Opportunity", value: 3 },
    ],
    // All the possible importances (common for both internal and external factors)
    possibleImportances: [
      { text: "Unimportant", value: 0 },
      { text: "Of Little Importance", value: 1 },
      { text: "Moderately Important", value: 2 },
      { text: "Important", value: 3 },
      { text: "Very Important", value: 4 },
    ],
  }),
  computed: {
    // Internal and external factors have different possible classifications
    // So the list of classifications needs to be filtered passed on the quadrants
    possibleClassifications() {
      // quadrant_1 and quadrant_2 are objects with name of quadrant
      // in plural form e.g (weaknessess) and quadrant id
      // To override the plural and singular diference, we can use the first letter (unique for every classification)
      const quadrant1_name = this.quadrant1.name;
      const possible_classification_1 = this.AllClassifications.filter(
        function (item) {
          return item.text.charAt(0) == quadrant1_name.charAt(0);
        }
      )[0];

      const quadrant2_name = this.quadrant2.name;
      const possible_classification_2 = this.AllClassifications.filter(
        function (item) {
          return item.text.charAt(0) == quadrant2_name.charAt(0);
        }
      )[0];
      return [possible_classification_1, possible_classification_2];
    },
  },

  methods: {
    // method for creating a factor
    async createFactor() {
      // Need to decide which quadrant the factor belongs
      const quadrant_id = this.whichQuadrant(this.factor.classification);

      // Send POST method to create factor
      try {
        await this.$axios.post(
          `/swot_analyses/${this.analysisId}/quadrants/${quadrant_id}/factors/`,
          this.factor
        );
      } catch (err) {
        this.$refs.observer.setErrors(err.response.data);
      }

      this.clearForm();
      //this.$axios.post("");
    },
    clearForm() {
      // First lets reset the form
      this.$refs.form.reset();
      // Reset error msgs
      this.$refs.observer.reset();
    },
    // Upon the user deciding the classification of the factor
    // we need to obtain which of the quadrants it belongs
    // We use the first letter of the decided classification
    // and match it against the 2 quadrants
    whichQuadrant(choosen_classification) {
      // `choosen_classification` is the integer part
      // We need to reverse it to text version
      const first_letter_choosen_classification = this.AllClassifications[
        parseInt(choosen_classification)
      ].text.charAt(0);

      // If the first letter of the choosen classification matches the first letter
      // of the first quadrant, we return that quadrant id
      if (
        first_letter_choosen_classification == this.quadrant1.name.charAt(0)
      ) {
        return this.quadrant1.id;
      }
      // else we return the id of quadrant 2
      return this.quadrant2.id;
    },
  },
};
</script>

<style></style>
