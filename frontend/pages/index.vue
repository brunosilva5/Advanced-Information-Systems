<template>
  <v-container fluid fill-height class="white">
    <v-row>
      <v-sheet class="mx-auto white" width="50%">
        <v-img contain src="/Logo/vector/default-monochrome-third.svg"> </v-img>
        <v-card-title class="justify-center pt-10">
          <div class="text-h3 first--text font-weight-regular">
            Welcome to SWOTLab!
          </div>
        </v-card-title>
        <v-card-subtitle
          class="first--text text-subtitle-1 font-weight-light text-justify pt-10"
        >
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque nisl
          eros, pulvinar facilisis justo mollis, auctor consequat urna. Morbi a
          bibendum metus. Donec scelerisque sollicitudin enim eu venenatis. Duis
          tincidunt laoreet ex, in pretium orci vestibulum eget. Class aptent
          taciti sociosqu ad litora torquent per conubia nostra, per inceptos
          himenaeos. Duis pharetra luctus lacus ut vestibulum. Maecenas ipsum
          lacus, lacinia quis posuere ut, pulvinar vitae dolor. Integer eu nibh
          at nisi ullamcorper sagittis id vel leo. Integer feugiat faucibus
          libero, at maximus nisl suscipit posuere.
        </v-card-subtitle>
        <v-card-actions class="justify-center pt-10">
          <v-btn
            nuxt
            depressed
            color="third white--text"
            x-large
            to="/dashboard"
          >
            <v-icon class="ma-2"> speed </v-icon>
            Get Started
          </v-btn>
        </v-card-actions>
      </v-sheet>
    </v-row>
  </v-container>
</template>

<script>
export default {
  layout: "empty",
};
</script>
