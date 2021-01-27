<template>
  <ValidationObserver ref="observer" v-slot="{ invalid }">
    <v-form @submit.prevent="createFactor">
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

  data: () => ({
    valid: false,
    factor: {
      description: null,
      importance: null,
      classification: null,
    },
    possibleClassifications: [
      { text: "Strength", value: 0 },
      { text: "Weakness", value: 1 },
    ],
    possibleImportances: [
      { text: "Unimportant", value: 0 },
      { text: "Of Little Importance", value: 1 },
      { text: "Moderately Important", value: 1 },
      { text: "Important", value: 1 },
      { text: "Very Important", value: 1 },
    ],
  }),
};
</script>

<style></style>
