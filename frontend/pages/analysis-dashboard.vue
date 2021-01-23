<template>
  <v-row class="mt-15" justify="center">
    <v-col class="text-center" cols="12" md="6">
      <v-card elevation="6">
        <v-card-title>
          <v-sheet
            color="forth"
            elevation="6"
            rounded
            class="mt-n12"
            height="100"
            width="100%"
          >
            <div class="text-h4 pa-8">{{ title }}</div></v-sheet
          >
          <v-spacer></v-spacer>
          <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            label="Search"
            single-line
            hide-details
          ></v-text-field>
        </v-card-title>
        <v-data-table
          :headers="headers"
          :items="desserts"
          :search="search"
        ></v-data-table>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  // This route required authentication
  middleware: "authenticated",
  data() {
    return {
      search: "",
      title: "My Analysis",
      headers: [
        {
          text: "Dessert (100g serving)",
          align: "start",
          sortable: false,
          value: "name",
        },
        { text: "Calories", value: "calories" },
        { text: "Fat (g)", value: "fat" },
        { text: "Carbs (g)", value: "carbs" },
        { text: "Protein (g)", value: "protein" },
        { text: "Iron (%)", value: "iron" },
      ],
      desserts: [
        {
          name: "Frozen Yogurt",
          calories: 159,
          fat: 6.0,
          carbs: 24,
          protein: 4.0,
          iron: "1%",
        },
      ],
    };
  },
};
</script>
