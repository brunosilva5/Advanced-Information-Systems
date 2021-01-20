<template>
  <v-app>
    <NavigationDrawer />
    <AppBar />
    <v-main>
      <nuxt-child />
    </v-main>
  </v-app>
</template>

<script>
import NavigationDrawer from "./NavigationDrawer";
import AppBar from "./AppBar";

export default {
  components: { NavigationDrawer, AppBar },
};
</script>
