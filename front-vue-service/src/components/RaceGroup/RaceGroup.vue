<template>
  <div>
    <a href="#" class="list-group-item list-group-item-action">
      <div class="d-flex w-100 justify-content-between">
        <h4 class="mb-0">{{racegroup.name}}</h4>
        <small>3 days ago</small>
      </div>
      <div class="row">
        <div class="col-sm">
          <small>races: 3</small>
          <small>results: 3920</small>
          <small>uniq runners: 1837</small>
        </div>
      </div>
    </a>
    <app-race v-for="race in racegroup.races" :race="race" v-bind:key="race.id"></app-race>
  </div>
</template>

<script>
import Race from "./Race.vue";

export default {
  props: ["racegroup"],
  components: {
    appRace: Race
  }
};
</script>

<style>
</style>
