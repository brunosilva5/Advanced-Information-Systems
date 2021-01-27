<template>
  <div>
    <v-app-bar app color="first" dense="">
      <template #img="{ props }">
        <v-img v-bind="props"></v-img>
      </template>

      <v-app-bar-nav-icon
        class="hidden-md-and-up white--text"
        @click="drawer = !drawer"
      />

      <v-app-bar-title class="white--text">
        <h2>{{ currentName }}</h2>
      </v-app-bar-title>

      <v-spacer></v-spacer>

      <v-menu left bottom offset-y v-if="$auth.loggedIn">
        <template #activator="{ on }">
          <v-hover>
            <v-chip
              slot-scope="{ hover }"
              v-ripple
              class="first white--text"
              :class="`elevation-${hover ? 5 : 2}`"
              v-on="on"
            >
              <v-avatar class="ma-2">
                <v-icon class="white--text">account_circle</v-icon>
              </v-avatar>
              {{ $auth.user.first_name }} {{ $auth.user.last_name }}
            </v-chip>
          </v-hover>
        </template>

        <v-list>
          <v-list-item
            v-for="(item, i) in bar_items"
            :key="i"
            :to="item.link"
            link
            nuxt
          >
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item>
          <!-- Logout option -->
          <v-divider></v-divider>
          <v-list-item @click="$auth.logout()">
            <v-list-item-title>Logout</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-navigation-drawer
      v-model="drawer"
      app
      :permanent="!$vuetify.breakpoint.xsOnly"
      class="first"
      :right="$vuetify.rtl"
    >
      <v-list-item class="py-5">
        <v-img src="/Logo/vector/default-monochrome-white.svg"></v-img>
      </v-list-item>

      <v-divider class="second"></v-divider>

      <v-list dense nav>
        <v-list-item-group v-model="selectedItem" color="primary">
          <v-list-item
            v-for="item in drawer_items"
            :key="item.title"
            :to="item.link"
            link
            nuxt
          >
            <v-list-item-icon>
              <v-icon class="white--text">{{ item.icon }}</v-icon>
            </v-list-item-icon>

            <v-list-item-content>
              <v-list-item-title class="white--text">{{
                item.title
              }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
      <template #append>
        <div class="pa-2">
          <v-btn block> Help center </v-btn>
        </div>
      </template>
    </v-navigation-drawer>
  </div>
</template>

<script>
export default {
  // Data
  data() {
    return {
      drawer: false,
      bar_items: [{ title: "My profile", link: "/profile" }],
      selectedItem: 0,
      drawer_items: [
        { title: "Analysis dashboard", icon: "dashboard", link: "/analysis" },
        { title: "Create analysis", icon: "add_box", link: "/analysis/new" },
      ],
      right: null,
    };
  },
  // Computed properties
  computed: {
    currentName() {
      const path = this.$nuxt.$route.path.split("/");
      let name = path[path.length - 1];
      return name.charAt(0).toUpperCase() + name.slice(1);
    },
  },
};
</script>

<style></style>
