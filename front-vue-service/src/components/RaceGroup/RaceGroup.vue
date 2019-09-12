<template>
  <div class="mb-2">
    <a
      href="#"
      class="list-group-item list-group-item-action main-group"
      @mouseover="showicons=true"
      @mouseleave="showicons=false"
    >
      <div class="d-flex w-100 justify-content-between">
        <h4 class="mb-0" v-if="!edit" @dblclick="edit=true">{{racegroup.name}}</h4>
        <app-race-group-form v-if="edit" :racegroup="racegroup" @raceGroupSaved="updateRaceGroup()"></app-race-group-form>
        <div>
          <small v-if="showicons && !edit">
            <a @click="addRace()">add race</a>
            |
            <a @click="edit=true">edit</a>
            |
            <a @click="deleteGroup">delete</a>
          </small>
        </div>
      </div>
      <div class="row">
        <div class="col-sm">
          <small>races: {{racegroup.races.length}}</small>
          <small>results: 3920</small>
          <small>uniq runners: 1837</small>
        </div>
      </div>
    </a>
    <app-race
      v-for="(race, index) in racegroup.races"
      :race="race"
      v-bind:key="race.id"
      @raceDelete="deleteRace(index, race)"
    ></app-race>
  </div>
</template>

<script>
import Race from "./Race.vue";
import RaceGroupForm from "./RaceGroupForm.vue";
import { raceEditBus } from "../../main.js";

export default {
  props: ["racegroup"],
  components: {
    appRace: Race,
    appRaceGroupForm: RaceGroupForm
  },
  methods: {
    addRace() {
      $("#raceFormModal").modal();
      let new_race = {};
      raceEditBus.$emit("add-race", {
        race: new_race,
        racegroup: this.racegroup
      });
    },
    updateRaceGroup() {
      this.edit = false;
      this.$emit("raceGroupUpdate", this.racegroup);
    },

    deleteGroup() {
      if (confirm("Delete race group " + this.racegroup.name + "?")) {
        this.$emit("raceGroupDelete", this.racegroup);
      } else {
        return false;
      }
    },
    deleteRace(index, race) {
      this.resource_race.delete({ race_id: race.id }).then(response => {
        this.racegroup.races.splice(index, 1);
      });
    }
  },

  data() {
    return {
      edit: false,
      showicons: false
    };
  },
  created() {
    this.resource_race = this.$resource(
      "http://localhost:8001/api/races{/race_id}/"
    );
  }
};
</script>

<style scoped>
a.list-group-item.main-group {
  background: rgb(241, 241, 241);
}
body {
  background: #666;
}
</style>>

