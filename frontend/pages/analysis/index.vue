<template>
  <v-container fluid fill-height>
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
                <!-- Delete dialog -->
                <v-dialog v-model="dialogDelete" max-width="500px">
                  <v-card>
                    <v-card-title class="headline"
                      >Are you sure you want to delete this
                      analysis?</v-card-title
                    >
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn
                        color="blue darken-1"
                        text
                        @click="closeDeleteDialog"
                        >Cancel</v-btn
                      >
                      <v-btn
                        color="blue darken-1"
                        text
                        @click="deleteAnalysisConfirm"
                        >OK</v-btn
                      >
                      <v-spacer></v-spacer>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </v-toolbar>
            </template>
            <!-- Custom Field Rendering -->
            <template #item="{ item, expand, isExpanded }">
              <tr>
                <td>
                  <v-icon @click="expand(!isExpanded)"
                    >keyboard_arrow_down</v-icon
                  >
                </td>
                <td class="font-weight-light">#{{ item.id }}</td>

                <td>
                  <v-btn text nuxt :to="'/analysis/' + item.id">{{
                    item.title
                  }}</v-btn>
                </td>
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
                  <v-icon small class="mr-2" @click="editAnalysis(item)">
                    edit
                  </v-icon>
                  <v-icon small class="mr-2" @click="archiveAnalysis(item)">
                    archive
                  </v-icon>
                  <v-icon small class="mr-2" @click="deleteAnalysis(item)">
                    delete
                  </v-icon>
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
  </v-container>
</template>

<script>
export default {
  // This route required authentication
  middleware: "authenticated",

  async asyncData({ $axios }) {
    const analyses = await $axios
      .get("/swot_analyses/")
      .then((res) => res.data);
    return { analyses };
  },
  data: () => ({
    expanded: [],
    title: "My analyses",
    search: "",
    dialog: false,
    headers: [
      { text: "", value: "id", align: "center", sortable: false },
      { text: "", value: "data-table-expand" },
      { text: "Title", value: "title", align: "center" },
      { text: "State", value: "state", align: "center" },
      { text: "Created at", value: "starting_date", align: "center" },
      { text: "Actions", value: "actions", sortable: false },
    ],
    dialogDelete: false,
    deleteId: null,
  }),
  head() {
    return {
      title: "Analysis dashboard",
    };
  },
  methods: {
    getColor(state) {
      if (state === "In progress") return "green";
      else return "red";
    },
    // Methods for deleting an analysis
    closeDeleteDialog() {
      this.dialogDelete = false;
    },
    deleteAnalysis(item) {
      this.dialogDelete = true;
      this.deleteId = item.id;
    },
    async deleteAnalysisConfirm() {
      this.closeDeleteDialog();
      await this.$axios.delete(`/swot_analyses/${this.deleteId}`);
      this.$nuxt.refresh();
    },
  },
};
</script>
