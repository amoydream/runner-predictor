<template>
  <div class="col-xs-12 col-sm-6">
    <p v-if="!racegroup">Please select a RaceGroup</p>
    <p v-else>RaceGroup #{{ racegroup.id }} selected, Status: {{ racegroup.status }}</p>
    <hr />
    <button v-if="racegroup" @click="resetStatus">Change to Normal</button>
  </div>
</template>

<script>
import { raceGroupBus } from "../../main";

export default {
  data: function() {
    return {
      racegroup: null
    };
  },
  methods: {
    resetStatus() {
      this.racegroup.status = "Normal";
    }
  },
  created() {
    raceGroupBus.$on("raceGroupSelecteded", racegroup => {
      console.log("racegroup2", racegroup.status);
      this.racegroup = racegroup;
    });
  }
};
</script>

<style>
</style>
