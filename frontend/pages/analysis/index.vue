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
                    <v-card-title
                      class="justify-center"
                      style="word-break: normal"
                    >
                      <div>Are you sure you want to delete this analysis?</div>
                    </v-card-title>
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
                <!-- Archive dialog -->
                <v-dialog v-model="dialogArchive" max-width="500px">
                  <v-card>
                    <v-card-title
                      class="justify-center"
                      style="word-break: normal"
                    >
                      <div>Are you sure you want to close this analysis?</div>
                    </v-card-title>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn
                        color="blue darken-1"
                        text
                        @click="closeArchiveDialog"
                        >Cancel</v-btn
                      >
                      <v-btn
                        color="blue darken-1"
                        text
                        @click="archiveAnalysisConfirm"
                        >OK</v-btn
                      >
                      <v-spacer></v-spacer>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
                <!-- Unarchive dialog -->
                <v-dialog v-model="dialogUnarchive" max-width="500px">
                  <v-card>
                    <v-card-title
                      class="justify-center"
                      style="word-break: normal"
                    >
                      <div>Are you sure you want to open this analysis?</div>
                    </v-card-title>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn
                        color="blue darken-1"
                        text
                        @click="closeUnarchiveDialog"
                        >Cancel</v-btn
                      >
                      <v-btn
                        color="blue darken-1"
                        text
                        @click="unarchiveAnalysisConfirm"
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
                  <v-tooltip bottom>
                    <template #activator="{ on, attrs }">
                      <v-icon
                        small
                        class="mr-2"
                        v-bind="attrs"
                        @click="editAnalysis(item)"
                        v-on="on"
                      >
                        edit
                      </v-icon>
                    </template>
                    <span>Edit</span>
                  </v-tooltip>
                  <!-- If open show archive icon -->
                  <span v-if="item.state === 'Open'">
                    <v-tooltip bottom>
                      <template #activator="{ on, attrs }">
                        <v-icon
                          small
                          v-bind="attrs"
                          class="mr-2"
                          v-on="on"
                          @click="archiveAnalysis(item)"
                        >
                          archive
                        </v-icon>
                      </template>
                      <span>Close</span>
                    </v-tooltip>
                  </span>
                  <span v-else>
                    <!-- If closed show unarchive icon -->
                    <v-tooltip bottom>
                      <template #activator="{ on, attrs }">
                        <v-icon
                          small
                          v-bind="attrs"
                          class="mr-2"
                          v-on="on"
                          @click="unarchiveAnalysis(item)"
                        >
                          unarchive
                        </v-icon>
                      </template>
                      <span>Open</span>
                    </v-tooltip>
                  </span>
                  <v-tooltip bottom>
                    <template #activator="{ on, attrs }">
                      <v-icon
                        small
                        v-bind="attrs"
                        class="mr-2"
                        v-on="on"
                        @click="deleteAnalysis(item)"
                      >
                        delete
                      </v-icon>
                    </template>
                    <span>Delete</span>
                  </v-tooltip>
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
    headers: [
      { text: "", value: "id", align: "center", sortable: false },
      { text: "", value: "data-table-expand" },
      { text: "Title", value: "title", align: "center" },
      { text: "State", value: "state", align: "center" },
      { text: "Created at", value: "starting_date", align: "center" },
      { text: "Actions", value: "actions", sortable: false },
    ],
    // Delete actions
    dialogDelete: false,
    deleteId: null,
    // Archive actions
    dialogArchive: false,
    archiveId: null,
    // Unarchive actions
    dialogUnarchive: false,
    unarchiveId: null,
  }),
  head() {
    return {
      title: "Analysis dashboard",
    };
  },

  methods: {
    getColor(state) {
      if (state === "Open") return "green";
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
    // Methods for archiving an analysis
    closeArchiveDialog() {
      this.dialogArchive = false;
    },
    archiveAnalysis(item) {
      this.dialogArchive = true;
      this.archiveId = item.id;
    },
    async archiveAnalysisConfirm() {
      this.closeArchiveDialog();
      const payload = { state: 2 };
      await this.$axios.patch(`/swot_analyses/${this.archiveId}`, payload);
      this.$nuxt.refresh();
    },
    // Methods for unarchiving an analysis
    closeUnarchiveDialog() {
      this.dialogUnarchive = false;
    },
    unarchiveAnalysis(item) {
      this.dialogUnarchive = true;
      this.unarchiveId = item.id;
    },
    async unarchiveAnalysisConfirm() {
      this.closeUnarchiveDialog();
      const payload = { state: 1 };
      await this.$axios.patch(`/swot_analyses/${this.unarchiveId}`, payload);
      this.$nuxt.refresh();
    },
  },
};
</script>
