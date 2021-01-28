<template>
  <ValidationObserver ref="observer" v-slot="{ invalid }">
    <v-container fluid fill-height>
      <v-row justify="center" align="center">
        <v-col cols="12" md="6">
          <v-card
            :loading="loading ? 'third' : null"
            class="mx-auto"
            width="500"
          >
            <v-card-title
              class="title font-weight-regular justify-space-between"
            >
              <div class="text-h4 font-weight-light" style="word-break: normal">
                {{ currentTitle }}
              </div>
              <v-avatar
                color="third lighten-2"
                class="subheading white--text"
                size="24"
                v-text="step"
              ></v-avatar>
            </v-card-title>

            <v-window v-model="step" touchless>
              <v-window-item :value="1">
                <v-card-text>
                  <form @submit.prevent="editAnalysis">
                    <ValidationProvider
                      v-slot="{ errors }"
                      name="title"
                      rules="required"
                    >
                      <v-text-field
                        v-model="payload.title"
                        counter
                        :error-messages="errors"
                        label="Name"
                        required
                      ></v-text-field>
                    </ValidationProvider>
                    <ValidationProvider v-slot="{ errors }" name="description">
                      <v-textarea
                        v-model="payload.description"
                        label="Short description"
                        counter
                        :error-messages="errors"
                        maxlength="300"
                      ></v-textarea>
                    </ValidationProvider>

                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn
                        depressed
                        color="third"
                        class="white--text"
                        :disabled="invalid"
                        type="submit"
                        >Edit</v-btn
                      >
                    </v-card-actions>
                  </form>
                </v-card-text>
              </v-window-item>
              <!-- Sucess message -->
              <v-window-item :value="2">
                <div class="pa-4 text-center">
                  <span class="font-weight-light">
                    You successfully edited the analysis "{{ payload.title }}".
                  </span>
                  <v-divider class="ma-4"></v-divider>

                  <v-btn
                    depressed
                    color="third"
                    class="white--text"
                    to="/analysis"
                    >Go back to dashboard</v-btn
                  >
                </div>
              </v-window-item>
            </v-window>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </ValidationObserver>
</template>

<script>
import { ValidationObserver, ValidationProvider } from "vee-validate";

export default {
  components: {
    ValidationObserver,
    ValidationProvider,
  },
  // This route required authentication
  middleware: "authenticated",

  async asyncData({ params, redirect, $axios }) {
    let Analysis = null;
    try {
      Analysis = await $axios
        .get(`/swot_analyses/${params.id}/`)
        .then((res) => res.data);
    } catch (err) {
      // If error redirect to analysis dashboard
      console.log(err);
      redirect("/analysis");
    }
    return { Analysis };
  },
  data: () => ({
    // Current step
    step: 1,
    loading: false,
    // Payload for PATCH
    payload: {
      title: null,
      description: null,
      // https://github.com/brunosilva5/Advanced-Information-Systems/issues/25
      state: null,
    },
  }),
  head() {
    return {
      title: "Edit SWOT analysis",
    };
  },
  computed: {
    currentTitle() {
      switch (this.step) {
        case 1:
          return "Edit SWOT analysis";
        default:
          return "Analysis edited with sucess";
      }
    },
    analysisId() {
      return this.$route.params.id;
    },
    // https://github.com/brunosilva5/Advanced-Information-Systems/issues/25
    currentState() {
      return this.Analysis.state == "Open" ? 1 : 2;
    },
  },
  mounted() {
    this.payload.title = this.Analysis.title;
    this.payload.description = this.Analysis.description;
    // https://github.com/brunosilva5/Advanced-Information-Systems/issues/25
    this.payload.state = this.currentState;
  },
  methods: {
    // Edit SWOT Analysis
    async editAnalysis() {
      this.loading = true;
      console.log(this.payload);
      try {
        await this.$axios
          .patch(`/swot_analyses/${this.analysisId}/`, this.payload)
          .then((res) => res.data);
        this.step++;
      } catch (error) {
        console.log(error);
        this.$refs.observer.setErrors(error.response.data);
      }
      this.loading = false;
    },
  },
};
</script>

<style></style>
