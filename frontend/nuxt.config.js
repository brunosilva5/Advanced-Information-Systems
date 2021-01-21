import colors from "vuetify/es5/util/colors";

export default {
  ssr: false,
  // Target: https://go.nuxtjs.dev/config-target
  target: "static",

  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    titleTemplate: "%s - SWOTLab",
    title: "SWOTLab",
    htmlAttrs: {
      lang: "en",
    },
    meta: [
      { charset: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      { hid: "description", name: "description", content: "" },
    ],
    link: [
      { rel: "icon", type: "image/x-icon", href: "/favicon.ico" },
      {
        rel: "stylesheet",
        href:
          "https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Material+Icons",
      },
    ],
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: ["~/plugins/vee-validate"],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/eslint
    "@nuxtjs/eslint-module",
    // https://go.nuxtjs.dev/vuetify
    "@nuxtjs/vuetify",
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/axios
    "@nuxtjs/axios",
    "@nuxtjs/auth-next",
  ],

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {
    baseURL: "https://swotlab.herokuapp.com/api",
    headers: {
      common: {
        Accept: "application/json, text/plain, */*",
      },
    },
  },

  // Vuetify module configuration: https://go.nuxtjs.dev/config-vuetify
  vuetify: {
    customVariables: ["~/assets/variables.scss"],
    theme: {
      dark: false,
      themes: {
        dark: {
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3,
        },
        light: {
          first: "#1b262c",
          second: "#0f4c75",
          third: "#3282b8",
          forth: "#bbe1fa",
        },
      },
    },
    icons: {
      iconfont: "md", // Material design icons
    },
  },

  auth: {
    strategies: {
      local: {
        scheme: "refresh",
        token: {
          property: "access",
          maxAge: 300,
          // type: 'Bearer'
        },
        refreshToken: {
          property: "refresh",
          data: "refresh",
          maxAge: 24 * 60 * 60,
        },
        user: {
          property: "",
          // autoFetch: true
        },
        endpoints: {
          login: {
            url: "/users/auth/login/",
            method: "post",
            propertyName: "access",
          },
          refresh: { url: "/users/auth/login/refresh/", method: "post" },
          user: { url: "/users/me/", method: "get", propertyName: "" },
          logout: false,
        },
        autoLogout: false,
      },
    },
    redirect: {
      login: "/auth/login",
      logout: "/",
      callback: "/",
      home: "/dashboard",
    },
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {},
};
