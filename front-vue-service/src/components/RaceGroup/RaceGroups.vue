<template>
  <div>
    <app-race-results-modal :results="race_results"></app-race-results-modal>
    <div class="row">
      <div class="col-sm">
        <div class="list-group mx-auto mt-4" style="max-width:800px;">
          <div class="card mb-2">
            <div class="card-body">
              <h5 class="card-title">Add Race Group</h5>
              <app-race-group-form :racegroup="new_race_group" @raceGroupSaved="save_group"></app-race-group-form>
            </div>
          </div>
          <app-race-group
            v-for="(racegroup, index) in racegroups"
            :racegroup="racegroup"
            v-bind:key="racegroup.id"
            @raceGroupDelete="deleteRaceGroup(index,racegroup)"
            @raceGroupUpdate="updateRaceGroup(racegroup)"
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
import RaceResultsModal from "./RaceResultsModal.vue";
import { raceEditBus } from "../../main.js";
import { raceResultBus } from "../../main.js";
export default {
  components: {
    AppRaceGroup: RaceGroup,
    AppRaceForm: RaceForm,
    AppRaceGroupForm: RaceGroupForm,
    AppRaceResultsModal: RaceResultsModal
  },
  created() {
    raceEditBus.$on("race-to-edit", race => {
      this.race_edited = race;
    });
    raceResultBus.$on("race-results-show", race_rasults => {
      this.race_results = race_rasults;
    });
    raceEditBus.$on("add-race", data => {
      this.race_edited = data.race;
      this.race_group_where_add_race = data.racegroup;
    });

    this.resource = this.$resource(
      "http://localhost:8001/api/race-group{/race_group_id}/"
    );
    this.resource
      .get()
      .then(response => {
        return response.json();
      })
      .then(data => {
        this.racegroups = data;
      });
  },
  methods: {
    save_group(data) {
      this.new_race_group = {};
      this.resource
        .save(data)
        .then(response => {
          return response.json();
        })
        .then(racegroup => {
          this.racegroups.push(racegroup);
        });
    },
    updateRaceGroup(racegroup) {
      this.resource
        .update({ race_group_id: racegroup.id }, racegroup)
        .then(response => {});
    },
    deleteRaceGroup(index, race_group) {
      this.resource.delete({ race_group_id: race_group.id }).then(response => {
        this.racegroups.splice(index, 1);
      });
    }
  },
  data: function() {
    return {
      resource: {},
      race_results: [],
      new_race_group: { races: [] },
      race_edited: {},
      race_group_where_add_race: {},
      racegroups: []
    };
  }
};
</script>

<style>
</style>
