<template>
  <v-container fill-height class="primary" fluid>
    <v-card class="mx-auto" width="500">
      <v-card-title class="title font-weight-regular justify-space-between">
        <p class="text-h3 font-weight-light">{{ currentTitle }}</p>
        <v-avatar
          color="primary lighten-2"
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
                        v-model="register.user.first_name"
                        :error-messages="errors"
                        label="Primeiro nome(s)*"
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
                        v-model="register.user.last_name"
                        :error-messages="errors"
                        label="Apelido(s)*"
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
                        v-model="register.user.email"
                        :error-messages="errors"
                        prepend-icon="email"
                        label="Email*"
                        hint="exemplo@email.com"
                        autocomplete="email"
                      ></v-text-field>
                    </ValidationProvider>
                  </v-col>

                  <!-- |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| -->
                  <!-- NIF -->
                  <v-col cols="12">
                    <ValidationProvider
                      v-slot="{ errors }"
                      vid="NIF"
                      name="NIF"
                      rules="required"
                    >
                      <v-text-field
                        v-model="register.NIF"
                        :error-messages="errors"
                        prepend-icon="perm_identity"
                        label="NIF*"
                        maxlength="9"
                        counter
                        hint="Número de Identificação Fiscal"
                      ></v-text-field>
                    </ValidationProvider>
                  </v-col>
                  <!-- |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| -->

                  <!-- Company -->
                  <v-col cols="12">
                    <ValidationProvider
                      v-slot="{ errors }"
                      vid="company"
                      name="Empresa"
                    >
                      <v-text-field
                        v-model="register.company"
                        :error-messages="errors"
                        prepend-icon="business"
                        label="Empresa"
                        hint="Campo opcional. A empresa onde trabalha."
                        autocomplete="organization"
                      ></v-text-field>
                    </ValidationProvider>
                  </v-col>
                  <!-- |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| -->

                  <!-- Phone number -->
                  <v-col cols="12">
                    <ValidationProvider
                      v-slot="{ errors }"
                      vid="phone_number"
                      name="Telemóvel"
                      rules="required"
                    >
                      <v-text-field
                        v-model="register.phone_number"
                        :error-messages="errors"
                        prepend-icon="phone"
                        maxlength="15"
                        label="Número telemóvel*"
                        hint="Indicativo por defeito: +351"
                        autocomplete="tel"
                      ></v-text-field>
                    </ValidationProvider>
                  </v-col>

                  <!-- Password -->
                  <v-col cols="12">
                    <ValidationProvider
                      v-slot="{ errors }"
                      vid="password"
                      name="Password"
                      rules="required"
                    >
                      <v-text-field
                        v-model="register.user.password"
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
                        v-model="register.user.confirm_password"
                        :error-messages="errors"
                        prepend-icon="vpn_key"
                        block
                        :append-icon="
                          show_register_password2
                            ? 'visibility'
                            : 'visibility_off'
                        "
                        :type="show_register_password2 ? 'text' : 'password'"
                        label="Confirmar Password*"
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
                      >Registar</v-btn
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
              src="https://marfonbackoffice.s3.eu-west-3.amazonaws.com/frontend_images/all_white.png"
            ></v-img>
            <h3 class="title font-weight-light mb-2">Bem-vindo ao Marfon!</h3>
            <span class="font-weight-light"
              >Obrigado por se registar! Para poder efetuar login com a sua
              conta por favor verifique a sua caixa de entrada.</span
            >
            <v-divider class="mx-4"></v-divider>

            <v-btn outlined nuxt :to="{ path: '/' }"
              >Carregue aqui para voltar ao início</v-btn
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
  // use the auth minimal layout
  layout: "auth",

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
      NIF: "",
      company: "",
      phone_number: "",
      user: {
        email: "",
        first_name: "",
        last_name: "",
        password: "",
        confirm_password: "",
      },
    },
  }),
  computed: {
    currentTitle() {
      switch (this.step) {
        case 1:
          return "Registar";
        default:
          return "Registo efetuado";
      }
    },
  },
  // Methods
  methods: {
    // Register user
    async registerUser() {
      try {
        await this.$axios.post("/clients/create/", this.register);
        this.step++;
      } catch (error) {
        // Email needs manual set
        if ("user" in error.response.data) {
          if ("email" in error.response.data.user) {
            this.$refs.registerForm.setErrors({
              email: error.response.data.user.email,
            });
          }
        }
        this.$refs.registerForm.setErrors(error.response.data);
      }
    },
  },
};
</script>

<style></style>
