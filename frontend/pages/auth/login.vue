<template>
  <v-container fill-height class="first" fluid>
    <v-card :loading="loading ? 'accent' : null" class="mx-auto px-4">
      <v-card-title class="first--text">
        <p class="text-h3 font-weight-light">Login</p>
      </v-card-title>
      <v-card-subtitle
        >New to SWOTLab?
        <NuxtLink to="/auth/register">Sign up now</NuxtLink></v-card-subtitle
      >
      <v-card-text>
        <ValidationObserver ref="loginForm" v-slot="{ invalid }">
          <v-form @submit.prevent="loginUser">
            <!-- End of login error handling -->
            <v-row>
              <!-- Email field -->
              <v-col cols="12">
                <ValidationProvider
                  ref="account"
                  v-slot="{ errors }"
                  vid="email"
                  name="Email"
                  rules="required|email"
                >
                  <v-text-field
                    v-model="login.email"
                    :error-messages="errors"
                    prepend-icon="email"
                    label="Email"
                    required
                    hint="exemplo@email.com"
                    autocomplete="email"
                  ></v-text-field>
                </ValidationProvider>
              </v-col>
              <!-- Password field -->
              <v-col cols="12">
                <ValidationProvider
                  v-slot="{ errors }"
                  vid="password"
                  name="Password"
                  rules="required"
                >
                  <v-text-field
                    v-model="login.password"
                    :error-messages="errors"
                    prepend-icon="vpn_key"
                    :append-icon="
                      show_login_password ? 'visibility' : 'visibility_off'
                    "
                    :type="show_login_password ? 'text' : 'password'"
                    label="Password"
                    autocomplete="current-password"
                    counter
                    @click:append="show_login_password = !show_login_password"
                  ></v-text-field>
                </ValidationProvider>
              </v-col>
              <v-spacer></v-spacer>
              <!-- Login button -->
              <v-col class="ml-auto text-right" cols="12" sm="3" xsm="12">
                <v-btn
                  depressed
                  color="third"
                  class="white--text"
                  :disabled="invalid"
                  type="submit"
                  >Entrar</v-btn
                >
              </v-col>
            </v-row>
          </v-form>
        </ValidationObserver>
      </v-card-text>
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
  // Use the empty  layout
  layout: "empty",
  // Only allow guest users to acess login
  middleware: "auth",
  auth: "guest",

  data: () => ({
    loading: false,
    // Property for showing password in login tab
    show_login_password: false,

    // Login Payload
    login: {
      email: "test@email.com",
      password: "test321123",
    },
  }),
  // Methods
  methods: {
    // Login user
    async loginUser() {
      this.loading = true;
      try {
        await this.$auth.loginWith("local", { data: this.login });
      } catch (error) {
        this.$refs.loginForm.setErrors({
          email: ["Email or password is incorrect."],
        });
      }
      this.loading = false;
    },
  },
};
</script>
