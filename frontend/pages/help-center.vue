<template>
  <v-container fluid fill-height class="first">
    <v-row class="mt-15 pa-3" justify="center" align="center">
      <v-col class="text-center" cols="12" md="10">
        <v-card height="600">
          <v-card-title class="second--text text-center justify-center py-6">
            <h1 class="font-weight-bold display-3">Help Center</h1>
          </v-card-title>
          <v-tabs v-model="currentTab" color="second" grow>
            <v-tab v-for="item in barItems" :key="item.title">
              {{ item.title }}
            </v-tab>
          </v-tabs>
          <v-tabs-items v-model="currentTab">
            <v-tab-item v-for="item in barItems" :key="item.currentTab">
              <v-card-text class="text-center py-10" v-text="item.description">
              </v-card-text>
              <v-row dense class="justify-center">
                <v-col v-for="card in item.cards" :key="card" :cols="3">
                  <v-card class="mx-auto mb-1" width="300" min-height="270">
                    <v-card-title
                      class="third--text justify-center"
                      v-text="card.title"
                    >
                    </v-card-title>
                    <v-card-text
                      class="first--text pt-3 text-justify"
                      v-text="card.body"
                    ></v-card-text>
                  </v-card>
                </v-col>
              </v-row>
            </v-tab-item>
          </v-tabs-items>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
export default {
  layout: "empty",
  data: () => ({
    currentTab: null,
    barItems: [
      {
        title: "Internal factors",
        description:
          "According to the SWOT analysis methodology, a company has 2 internal factors: strengths and weaknesses.",
        cards: [
          {
            title: "Strengths",
            body:
              "Define the list with strengths identified in the company (differentiated team, innovative product, etc.).",
          },
          {
            title: "Weaknesses",
            body:
              "Define the list with the weaknesses (geographic location, high payroll, etc.)",
          },
        ],
      },
      {
        title: "External factors",
        description:
          "Once you have defined the internal factors, define the external ones: opportunities and threats.",
        cards: [
          {
            title: "Opportunities",
            body:
              "Define the list with the opportunities (expansion to strategic locations, new niche, etc.).",
          },
          {
            title: "Threats",
            body:
              "Define the list with the threats identified in the market (new competitors, tax changes, etc.).",
          },
        ],
      },
      {
        title: "SWOT matrix",
        description:
          "In this part of the spreadsheet you will be able to view an overview of your score for strengths, weaknesses, opportunities and threats. From this view, you will have the return of the spreadsheet on what time the company is going (development, maintenance, growth and survival). In addition to the indicators, also see the list with all the strengths, weaknesses, threats and opportunities ranked according to your score.",
      },
      {
        title: "Data crossing",
        description:
          "Once your internal and external factors have been defined, it is time to cross-check the data by combining your strengths and weaknesses with threats and opportunities. You can draw up an action plan for each combination.",
        cards: [
          {
            title: "Strengths + Opportunities",
            body:
              "The spreadsheet will show your 4 main strengths so that you can select an opportunity to combine. Draw a plan to get the best out of this combination.",
          },
          {
            title: "Strengths + Threats",
            body:
              "Your strength can be weakened by a threat. Select a threat that could damage your strength and define a containment plan to prevent problems from happening.",
          },
          {
            title: "Weaknesses + Opportunities",
            body:
              "A weakness of yours can be minimized by some opportunity. Make this combination and draw up a plan on how to take advantage of an opportunity by minimizing a weakness.",
          },
          {
            title: "Weaknesses + Threats",
            body:
              "Weaknesses and threats represent the greatest risk that a company can take. Combine some threats with your weaknesses and devise a plan to contain possible problems.",
          },
        ],
      },
      {
        title: "Graphics",
        description:
          "The graphics are important for them to be made assessments of the time the company and the comparison of their strengths, weaknesses, opportunities and threats. See also the graph with the favorability index and the graph about the current moment of the company",
      },
      {
        title: "Recommendations",
        description:
          "This spreadsheet will evaluate all the data you have filled in and will return with important tips for your SWOT analysis. This return will be displayed by balancing strengths, weaknesses, opportunities and threats.",
      },
      {
        title: "Printable report",
        description:
          "Print only what matters. This part generates a report formatted for printing on 7 A4 pages with its action plan for all combinations of strengths, weaknesses, opportunities and threats. In addition, have the graphics, the hierarchical list, the favorability index and the tips.",
      },
    ],
  }),
};
</script>
