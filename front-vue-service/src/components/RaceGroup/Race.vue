<template>
  <div>
    <a
      href="#"
      class="list-group-item list-group-item-action"
      @mouseover="showicons=true"
      @mouseleave="showicons=false"
    >
      <div class="row mt-2 pb-2">
        <div class="col-sm">
          <div class="race-header">{{race.name}}</div>

          <small>start date: {{race.start_date | toDbDateFormat}}</small>
          <small>results: {{race.results_count}}</small>
          <small>distance: {{race.distance}}km</small>
          <small>elevation: +{{race.elevation_gain}} -{{race.elevation_lost}}</small>
          <br />
          <small>food point: {{race.food_point}}</small>
          <small>time limit: {{race.time_limit}}h</small>
          <small>itra race id: {{race.itra_race_id}}</small>
        </div>
      </div>
      <small v-if="showicons" class="edit-link">
        <a @click="show_form_modal()">edit</a>
      </small>
    </a>
  </div>
</template>

<script>
import { raceEditBus } from "../../main.js";
export default {
  props: ["race"],
  methods: {
    show_form_modal() {
      $("#raceFormModal").modal();
      raceEditBus.$emit("race-to-edit", this.race);
    }
  },
  data() {
    return {
      edit: false,
      showicons: false
    };
  },
  filters: {
    toDbDateFormat(date) {
      if (Object.prototype.toString.call(date) === "[object Date]") {
        return date.toISOString().substring(0, 10);
      } else {
        return date;
      }
    }
  }
};
</script>
<style lang="scss" scoped>
.edit-link {
  position: absolute;
  top: 10px;
  right: 10px;
}
</style>
