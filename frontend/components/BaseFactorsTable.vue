<template>
  <v-data-table :headers="headers" :items="factors" class="elevation-1">
    <template #top>
      <v-toolbar flat>
        <v-toolbar-title>Create Factor</v-toolbar-title>
        <v-divider class="mx-4" inset vertical></v-divider>
        <!-- Only render create form is analysis is open -->
        <div v-if="canUserEdit">
          <FactorForm :possible-classifications="possibleClassifications" />
        </div>
        <v-dialog v-model="dialogDelete" max-width="500px">
          <v-card>
            <v-card-title class="justify-center" style="word-break: normal">
              <div>Are you sure you want to delete this factor?</div>
            </v-card-title>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="closeDeleteDialog"
                >Cancel</v-btn
              >
              <v-btn color="blue darken-1" text @click="deleteFactorConfirm">
                OK
              </v-btn>
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
    <!-- Custom field rendering -->
    <template #item="{ item }">
      <tr>
        <td>{{ item.description }}</td>
        <td>
          <v-chip :color="getClassificationColor(item.classification)" dark>
            {{ item.classification }}
          </v-chip>
        </td>
        <td>
          <v-chip :color="getImportanceColor(item.importance)" dark>
            {{ item.importance }}
          </v-chip>
        </td>
        <td>
          {{ item.score }}
        </td>
        <!-- Only render delete action if analysis is open -->
        <td v-if="canUserEdit">
          <v-tooltip bottom>
            <template #activator="{ on, attrs }">
              <v-icon
                small
                v-bind="attrs"
                class="mr-2"
                v-on="on"
                @click="deleteFactor(item)"
              >
                delete
              </v-icon>
            </template>
            <span>Delete</span>
          </v-tooltip>
        </td>
      </tr>
    </template>
  </v-data-table>
</template>

<script>
import FactorForm from "~/components/FactorForm";

export default {
  components: {
    FactorForm,
  },
  props: {
    // Possible classifications needs to be passed as prop because it's dynamic
    possibleClassifications: {
      type: Array,
      required: true,
    },
    // List of factors to display
    factors: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    default_headers: [
      { text: "Description", value: "description" },
      { text: "Classification", value: "classification" },
      { text: "Importance", value: "importance" },
      { text: "Score", value: "score" },
    ],
    // Delete actions
    dialogDelete: false,
    deleteFactorInstance: null,
    // Boolean variable to check if user can edit the analysis
    canUserEdit: false,
  }),
  async fetch() {
    // Fetch API to check if analysis if open or closed
    const analysis = await this.$axios
      .get(`/swot_analyses/${this.analysisId}/`)
      .then((res) => res.data);
    this.canUserEdit = analysis.state == "Open";
  },
  computed: {
    // Get analysis id from url
    analysisId() {
      return this.$route.params.id;
    },
    headers() {
      // Copy array
      const new_headers = [...this.default_headers];
      if (this.canUserEdit) {
        new_headers.push({
          text: "Actions",
          value: "actions",
          sortable: false,
        });
      }
      return new_headers;
    },
  },
  methods: {
    // method for deciding the color of v-chip based on classification
    getClassificationColor(value) {
      switch (value) {
        case "Strength":
        case "Opportunity":
          return "green";
        case "Threat":
        case "Weakness":
          return "red";
      }
    },
    // Methods for deleting a factor
    closeDeleteDialog() {
      this.dialogDelete = false;
    },
    deleteFactor(item) {
      this.dialogDelete = true;
      this.deleteFactorInstance = item;
    },
    async deleteFactorConfirm() {
      this.closeDeleteDialog();
      await this.$axios.delete(
        `/swot_analyses/${this.analysisId}/quadrants/${this.deleteFactorInstance.quadrant}/factors/${this.deleteFactorInstance.id}`
      );
      this.$nuxt.refresh();
    },
    // method for deciding the color of v-chip based on importance
    getImportanceColor(value) {
      switch (value) {
        case "Unimportant":
          return "red";
        case "Of Little Importance":
          return "orange";
        case "Moderately Important":
          return "grey darken-1";
        case "Important":
          return "green lighten-2";
        case "Very Important":
          return "green";
      }
    },
  },
};
</script>
