<template>
  <v-row class="mt-15 pa-3" justify="center" align="center">
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
            append-icon="search"
            label="Search"
            single-line
            hide-details
          ></v-text-field>
        </v-card-title>
        <!-- Start of table -->
        <v-data-table
          :headers="headers"
          :items="analyses"
          :search="search"
          show-expand
          single-expand
          :expanded.sync="expanded"
          item-key="id"
        >
          <template #top>
            <v-toolbar flat>
              <v-spacer></v-spacer>
              <v-btn
                depressed
                color="third"
                dark
                class="mb-2"
                nuxt
                to="/analysis/new"
              >
                Create Analysis
              </v-btn>
            </v-toolbar>
          </template>
          <!-- Custom Field Rendering -->
          <template #item="{ item, expand, isExpanded }">
            <tr>
              <td class="font-weight-light">#{{ item.id }}</td>
              <td>{{ item.title }}</td>
              <td>
                <v-chip :color="getColor(item.state)" dark>
                  {{ item.state }}
                </v-chip>
              </td>
              <td>
                {{
                  new Date(item.starting_date).toLocaleDateString("en-en", {
                    year: "numeric",
                    month: "short",
                    day: "numeric",
                  })
                }}
              </td>
              <td>
                <v-icon @click="expand(!isExpanded)"
                  >keyboard_arrow_down</v-icon
                >
              </td>
            </tr>
          </template>

          <!-- Now we choose what shows up in the expandable -->
          <template #expanded-item="{ headers, item }">
            <td :colspan="headers.length">{{ item.description }}</td>
          </template>
          <!-- END OF FIELDS -->
        </v-data-table>
        <!-- End of table -->
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  // This route required authentication
  middleware: "authenticated",
  data: () => ({
    expanded: [],
    title: "My analyses",
    search: "",
    dialog: false,
    dialogDelete: false,
    headers: [
      { text: "", value: "id", align: "center", sortable: false },
      { text: "Title", value: "title", align: "center" },
      { text: "State", value: "state", align: "center" },
      { text: "Created at", value: "starting_date", align: "center" },
      { text: "", value: "data-table-expand" },
    ],
    analyses: [],
  }),

  created() {
    this.initialize();
  },

  methods: {
    initialize() {
      // Get analyses from current user
      this.analyses = this.$auth.user.analyses;
    },
    getColor(state) {
      if (state === "In progress") return "green";
      else return "red";
    },
  },
};
</script>
