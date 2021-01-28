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
            <v-select
              v-model="factor.importance"
              item-text="text"
              item-value="value"
              :items="possibleImportances"
              :error-messages="errors"
              label="Importance"
            ></v-select>
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
    // Possible classifications needs to be passed as prop because it's dynamic
    possibleClassifications: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    valid: false,
    factor: {
      description: null,
      importance: null,
      classification: null,
    },
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
    // Get analysis id from url
    analysisId() {
      return this.$route.params.id;
    },
  },

  methods: {
    // method for creating a factor
    async createFactor() {
      // Get quadrant id
      const quadrant_id = this.possibleClassifications.filter((item) => {
        return item.value == this.factor.classification;
      })[0].quadrant_id;

      // Send POST method to create factor belonging to quadrant
      try {
        await this.$axios.post(
          `/swot_analyses/${this.analysisId}/quadrants/${quadrant_id}/factors/`,
          this.factor
        );
      } catch (err) {
        this.$refs.observer.setErrors(err.response.data);
      }
      // Make nuxt refresh the contents of the page
      this.$nuxt.refresh();
      this.clearForm();
    },
    clearForm() {
      // First lets reset the form
      this.$refs.form.reset();
      // Reset error msgs
      this.$refs.observer.reset();
    },
  },
};
</script>

<style></style>
