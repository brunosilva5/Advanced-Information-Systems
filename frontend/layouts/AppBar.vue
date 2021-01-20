<template>
  <div>
    <v-app-bar absolute app color="third" shrink-on-scroll>
      <template #img="{ props }">
        <v-img
          v-bind="props"
          gradient="to top right, rgba(19,84,122,.2), rgba(128,208,199,.6)"
        ></v-img>
      </template>

      <v-app-bar-nav-icon></v-app-bar-nav-icon>

      <v-app-bar-title>{{ currentName }}</v-app-bar-title>

      <v-spacer></v-spacer>

      <v-btn icon>
        <v-icon>search</v-icon>
      </v-btn>

      <v-btn icon>
        <v-icon>mdi-heart</v-icon>
      </v-btn>

      <v-menu left bottom offset-y>
        <template #activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" v-on="on">
            <v-icon>account_circle</v-icon>
          </v-btn>
        </template>

        <v-list>
          <v-list-item v-for="n in 5" :key="n" @click="() => {}">
            <v-list-item-title>Option {{ n }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>
  </div>
</template>

<script>
export default {
  computed: {
    currentName() {
      return this.$route.fullPath;
    },
  },
};
</script>

<style></style>
