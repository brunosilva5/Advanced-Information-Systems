<template>
  <div>
    <v-navigation-drawer app permanent class="first">
      <v-list-item class="py-5" nuxt link to="/">
        <v-img src="/Logo/vector/default-monochrome-white.svg"></v-img>
      </v-list-item>

      <v-divider class="second"></v-divider>

      <v-list dense nav>
        <v-list-item v-for="item in items" :key="item.title" link>
          <v-list-item-icon>
            <v-icon class="white--text">{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title class="white--text">{{
              item.title
            }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
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
  data() {
    return {
      items: [{ title: "Analysis dashboard", icon: "dashboard" }],
      right: null,
    };
  },
};
</script>

<style></style>
