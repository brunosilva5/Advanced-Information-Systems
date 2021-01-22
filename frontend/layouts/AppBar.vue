<template>
  <div>
    <v-app-bar absolute app color="third" dense="">
      <template #img="{ props }">
        <v-img
          v-bind="props"
          gradient="to top right, rgba(19,84,122,.2), rgba(128,208,199,.6)"
        ></v-img>
      </template>

      <v-app-bar-nav-icon></v-app-bar-nav-icon>

      <v-app-bar-title>
        <h2>{{ currentName }}</h2>
      </v-app-bar-title>

      <v-spacer></v-spacer>

      <v-menu left bottom offset-y>
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
            v-for="(item, i) in items"
            :key="i"
            @click="item.on_click"
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
  </div>
</template>

<script>
export default {
  // Data
  data() {
    return {
      items: [
        { title: "My profile" },
        { title: "Click Me" },
        { title: "Click Me" },
        { title: "Click Me 2" },
      ],
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
