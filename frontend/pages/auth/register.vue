<template>
  <v-container fill-height class="first" fluid>
    <v-card class="mx-auto" width="500">
      <v-card-title class="title font-weight-regular justify-space-between">
        <div class="text-h4 font-weight-light">{{ currentTitle }}</div>
        <v-avatar
          color="third lighten-2"
          class="subheading white--text"
          size="24"
          v-text="step"
        ></v-avatar>
      </v-card-title>

      <v-window v-model="step">
        <v-window-item :value="1">
          <!-- Personal Information -->
          <v-card-text>
            <ValidationObserver ref="registerForm" v-slot="{ invalid }">
              <v-form @submit.prevent="registerUser">
                <v-row>
                  <!-- First name -->
                  <v-col cols="12">
                    <ValidationProvider
                      v-slot="{ errors }"
                      vid="first_name"
                      name="First name"
                      rules="required"
                    >
                      <v-text-field
                        v-model="register.first_name"
                        :error-messages="errors"
                        label="First name*"
                        maxlength="20"
                        autocomplete="given-name"
                      ></v-text-field>
                    </ValidationProvider>
                  </v-col>
                  <!-- |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| -->
                  <!-- Last name -->
                  <v-col cols="12">
                    <ValidationProvider
                      v-slot="{ errors }"
                      vid="last_name"
                      name="Last name"
                      rules="required"
                    >
                      <v-text-field
                        v-model="register.last_name"
                        :error-messages="errors"
                        label="Last name*"
                        autocomplete="family-name"
                      ></v-text-field>
                    </ValidationProvider>
                  </v-col>
                  <!-- |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| -->
                  <!-- Email -->
                  <v-col cols="12">
                    <ValidationProvider
                      v-slot="{ errors }"
                      vid="email"
                      name="Email"
                      rules="required|email"
                    >
                      <v-text-field
                        v-model="register.email"
                        :error-messages="errors"
                        prepend-icon="email"
                        label="Email*"
                        hint="example@email.com"
                        autocomplete="email"
                      ></v-text-field>
                    </ValidationProvider>
                  </v-col>

                  <!-- |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| -->

                  <!-- Password -->
                  <v-col cols="12">
                    <ValidationProvider
                      v-slot="{ errors }"
                      vid="password"
                      name="Password"
                      rules="required"
                    >
                      <v-text-field
                        v-model="register.password"
                        :error-messages="errors"
                        prepend-icon="vpn_key"
                        :append-icon="
                          show_register_password1
                            ? 'visibility'
                            : 'visibility_off'
                        "
                        :type="show_register_password1 ? 'text' : 'password'"
                        label="Password*"
                        counter
                        autocomplete="new-password"
                        @click:append="
                          show_register_password1 = !show_register_password1
                        "
                      ></v-text-field>
                    </ValidationProvider>
                  </v-col>
                  <!-- |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| -->

                  <!-- Confirm password -->
                  <v-col cols="12">
                    <ValidationProvider
                      v-slot="{ errors }"
                      vid="confirm_password"
                      name="Confirmar password"
                      rules="required"
                    >
                      <v-text-field
                        v-model="register.confirm_password"
                        :error-messages="errors"
                        prepend-icon="vpn_key"
                        block
                        :append-icon="
                          show_register_password2
                            ? 'visibility'
                            : 'visibility_off'
                        "
                        :type="show_register_password2 ? 'text' : 'password'"
                        label="Confirm Password*"
                        counter
                        autocomplete="new-password"
                        @click:append="
                          show_register_password2 = !show_register_password2
                        "
                      ></v-text-field>
                    </ValidationProvider>
                  </v-col>

                  <v-spacer></v-spacer>
                  <v-col class="ml-auto text-right" cols="12" sm="3" xsm="12">
                    <v-btn
                      depressed
                      color="primary"
                      type="submit"
                      :disabled="invalid"
                      >Register</v-btn
                    >
                  </v-col>
                </v-row>
              </v-form>
            </ValidationObserver>
          </v-card-text>
        </v-window-item>

        <!-- Welcome message -->
        <v-window-item :value="2">
          <div class="pa-4 text-center">
            <v-img
              class="mb-4"
              contain
              height="128"
              src="/Logo/vector/default-monochrome-black.svg"
            ></v-img>
            <h3 class="title font-weight-light mb-2">Welcome to SWOTLab!</h3>
            <span class="font-weight-light">
              Thank you for registering! In order to log in with your account
              please confirm your email.</span
            >
            <v-divider class="ma-4"></v-divider>

            <v-btn
              depressed
              color="third"
              class="white--text"
              nuxt
              :to="{ path: '/auth/login' }"
              >Click here to login</v-btn
            >
          </div>
        </v-window-item>
      </v-window>
    </v-card>
  </v-container>
</template>

<script>
import { ValidationProvider, ValidationObserver } from "vee-validate";

export default {
  components: {
    ValidationProvider,
    ValidationObserver,
  },
  // use no layout
  layout: "empty",

  //middleware: ["not_authenticated"],
  data: () => ({
    // Property for showing password 1
    show_register_password1: false,
    // Property for showing password 2
    show_register_password2: false,
    // Property for loading
    loading: false,
    // Current step
    step: 1,
    // Register payload
    register: {
      email: "",
      first_name: "",
      last_name: "",
      password: "",
      confirm_password: "",
    },
  }),
  computed: {
    currentTitle() {
      switch (this.step) {
        case 1:
          return "Register";
        default:
          return "Registration Successful";
      }
    },
  },
  // Methods
  methods: {
    // Register user
    async registerUser() {
      try {
        await this.$axios.post("/users/create/", this.register);
        this.step++;
      } catch (error) {
        this.$refs.registerForm.setErrors(error.response.data);
      }
    },
  },
};
</script>
