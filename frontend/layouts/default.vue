<template>
  <v-app>
    <AppBar />
    <v-main>
      <nuxt-child />
    </v-main>
  </v-app>
</template>

<script>
import AppBar from "./AppBar";

export default {
  components: { AppBar },
};
</script>
