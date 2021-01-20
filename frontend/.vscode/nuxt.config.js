export default {
  // Target (https://go.nuxtjs.dev/config-target)
  target: "static",

  // Global page headers (https://go.nuxtjs.dev/config-head)
  head: {
    titleTemplate: "Marfon",
    title: "Marfon",
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

  // Global CSS (https://go.nuxtjs.dev/config-css)
  css: [],

  // Plugins to run before rendering page (https://go.nuxtjs.dev/config-plugins)
  plugins: ["~plugins/content.js", "~plugins/csrf.js"],

  // Auto import components (https://go.nuxtjs.dev/config-components)
  components: true,

  // Modules for dev and build (recommended) (https://go.nuxtjs.dev/config-modules)
  buildModules: [
    // https://go.nuxtjs.dev/vuetify
    "@nuxtjs/vuetify",
  ],

  // Modules (https://go.nuxtjs.dev/config-modules)
  modules: [
    // https://go.nuxtjs.dev/axios
    "@nuxtjs/axios",
    "@nuxtjs/auth-next",
  ],

  // Axios module configuration (https://go.nuxtjs.dev/config-axios)
  axios: {
    baseURL: "https://marfon-backend.herokuapp.com/api",
    headers: {
      common: {
        Accept: "application/json, text/plain, */*",
      },
    },
  },

  // Vuetify module configuration (https://go.nuxtjs.dev/config-vuetify)
  vuetify: {
    customVariables: ["~/assets/variables.scss"],
    theme: {
      themes: {
        light: {
          primary: "#303841",
          secondary: "#3a4750",
          accent: "#d72323",
          primary_light: "#eeeeee",
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
            url: "/clients/auth/login/",
            method: "post",
            propertyName: "access",
          },
          refresh: { url: "/clients/auth/login/refresh/", method: "post" },
          user: { url: "/clients/me/", method: "get", propertyName: "" },
          logout: false,
        },
        autoLogout: false,
      },
    },
  },

  // Build Configuration (https://go.nuxtjs.dev/config-build)
  build: {},
};
