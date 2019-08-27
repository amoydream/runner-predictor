<template>
  <div class="container">
    <app-header></app-header>
    <app-race-groups></app-race-groups>
  </div>
</template>

<script>
import Header from "./components/Shared/Header.vue";
import RaceGroups from "./components/RaceGroup/RaceGroups.vue";

export default {
  components: {
    appHeader: Header,
    appRaceGroups: RaceGroups
  }
};
</script>

<style>
</style>
