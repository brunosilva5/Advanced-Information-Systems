<template>
  <v-card>
    <v-card-title class="pa-0">
      <v-app-bar dense flat :class="color + ' lighten-1'">
        <div class="h2 font-weight-light">{{ quadrant.title }}</div>
        <v-spacer></v-spacer>
        <div class="h2 font-weight-light">{{ quadrant.total_score }}</div>
      </v-app-bar>
    </v-card-title>
    <v-data-table
      :items="quadrant.factors"
      hide-default-footer
      hide-default-header
    >
      <!-- Custom Field Rendering -->
      <template #item="{ item }">
        <tr>
          <td>{{ item.description }}</td>
          <td class="font-weight-light">
            <v-row justify="end" class="pa-3"> {{ item.score }} </v-row>
          </td>
        </tr>
      </template>
    </v-data-table>
  </v-card>
</template>
<script>
export default {
  props: {
    quadrant: {
      type: Object,
      required: true,
    },
    color: {
      type: String,
      required: true,
    },
  },
};
</script>
