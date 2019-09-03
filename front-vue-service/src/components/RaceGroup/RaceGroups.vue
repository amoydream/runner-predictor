<template>
  <div>
    <div class="row">
      <div class="col-sm">
        <div class="list-group mx-auto mt-4" style="max-width: 500px;">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Add Group</h5>
              <app-race-group-form :racegroup="new_race_group" @raceGroupSaved="save_group"></app-race-group-form>
            </div>
          </div>
          <app-race-group
            v-for="racegroup in racegroups"
            :racegroup="racegroup"
            v-bind:key="racegroup.id"
          ></app-race-group>
          <app-race-form :race="race_edited" :racegroup="race_group_where_add_race"></app-race-form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import RaceGroup from "./RaceGroup.vue";
import RaceForm from "./RaceForm.vue";
import RaceGroupForm from "./RaceGroupForm.vue";
import { raceEditBus } from "../../main.js";
export default {
  components: {
    AppRaceGroup: RaceGroup,
    AppRaceForm: RaceForm,
    AppRaceGroupForm: RaceGroupForm
  },
  created() {
    raceEditBus.$on("race-to-edit", race => {
      this.race_edited = race;
    });
    raceEditBus.$on("add-race", data => {
      this.race_edited = data.race;
      this.race_group_where_add_race = data.racegroup;
    });
  },
  methods: {
    save_group(data) {
      this.racegroups.push(data);
      this.new_race_group = {};
    }
  },
  data: function() {
    return {
      new_race_group: { races: [] },
      race_edited: {},
      race_group_where_add_race: {},
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
              itra: 2,
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
              itra: 2,
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
              itra: 2,
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
              itra: 2,
              food_point: 3,
              time_limit: 9,
              itra_race_id: 43397
            }
          ]
        }
      ]
    };
  }
};
</script>

<style>
</style>
