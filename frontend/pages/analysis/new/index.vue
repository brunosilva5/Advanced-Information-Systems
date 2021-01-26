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
                  <form @submit.prevent="createAnalysis">
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
                        >Create</v-btn
                      >
                    </v-card-actions>
                  </form>
                </v-card-text>
              </v-window-item>

              <!-- Welcome message -->
              <v-window-item :value="2">
                <div class="pa-4 text-center">
                  <span class="font-weight-light">
                    You successfully created analysis "{{ payload.title }}". You
                    can start working on it right away!
                  </span>
                  <v-divider class="ma-4"></v-divider>

                  <v-btn
                    depressed
                    color="third"
                    class="white--text"
                    nuxt
                    :to="{ path: '/analysis/', params: { id: id } }"
                    >Start working</v-btn
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
  data: () => ({
    // Current step
    id: null,
    step: 1,
    loading: false,
    payload: {
      title: "",
      description: null,
      state: 1, // 1=In progress https://github.com/brunosilva5/Advanced-Information-Systems/issues/22
    },
  }),
  head() {
    return {
      title: "Create SWOT analysis",
    };
  },
  computed: {
    currentTitle() {
      switch (this.step) {
        case 1:
          return "Create SWOT analysis";
        default:
          return "Analysis creation successful";
      }
    },
  },
  methods: {
    // Create SWOT Analysis
    async createAnalysis() {
      this.loading = true;
      try {
        const response = await this.$axios.post(
          "/swot_analyses/",
          this.payload
        );
        this.id = response.data.id;
        this.step++;
      } catch (error) {
        // Email needs manual set
        console.log(error);
      }
      this.loading = false;
    },
  },
};
</script>

<style></style>
