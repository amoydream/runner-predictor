<template>
  <div class="row">
    <div class="col-sm">
      <div class="list-group mx-auto mt-4" style="max-width: 500px;">
        <race-group
          v-for="racegroup in racegroups"
          :racegroup="racegroup"
          v-bind:key="racegroup.id"
        ></race-group>
      </div>
    </div>
  </div>
</template>

<script>
import RaceGroup from "./RaceGroup.vue";

export default {
  data: function() {
    return {
      racegroups: [
        {
          id: 1,
          name: "Wielka Prehyba!!",
          races: [
            {
              id: 3,
              name: "Wielka Prohyba 2019",
              start_date: "2019-04-12",
              results_count: 1120,
              distance: 43,
              elevation_gain: 1980,
              elevation_lost: 1980,
              food_point: 3,
              time_limit: 9,
              itra_race_id: 43397
            },
            {
              id: 4,
              name: "Wielka Prohyba 2018",
              start_date: "2018-04-12",
              results_count: 1920,
              distance: 43,
              elevation_gain: 1980,
              elevation_lost: 1980,
              food_point: 3,
              time_limit: 9,
              itra_race_id: 43397
            }
          ]
        },
        {
          id: 2,
          name: "Wielka Prehyba!!",
          races: [
            {
              id: 1,
              name: "Wielka Prohyba 2019",
              start_date: "2019-04-12",
              results_count: 1120,
              distance: 43,
              elevation_gain: 1980,
              elevation_lost: 1980,
              food_point: 3,
              time_limit: 9,
              itra_race_id: 43397
            },
            {
              id: 2,
              name: "Wielka Prohyba 2018",
              start_date: "2018-04-12",
              results_count: 1920,
              distance: 43,
              elevation_gain: 1980,
              elevation_lost: 1980,
              food_point: 3,
              time_limit: 9,
              itra_race_id: 43397
            }
          ]
        }
      ]
    };
  },
  components: {
    RaceGroup
  }
};
</script>

<style>
</style>
