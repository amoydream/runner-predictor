<template>
  <div>
    <div
      class="modal fade"
      id="raceFormModal"
      tabindex="-1"
      role="dialog"
      aria-labelledby="raceFormModal"
      aria-hidden="true"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-body">
            <form>
              <div class="form-group">
                <label for="exampleInputEmail1">Name</label>
                <input type="text" class="form-control" v-model="race.name" />
              </div>
              <div class="form-group">
                <datepicker
                  @input="race.start_date = formatDate($event)"
                  placeholder="Select Date"
                  v-model="race.start_date"
                  format="yyyy-MM-dd"
                  :bootstrap-styling="true"
                ></datepicker>
              </div>
              <div class="form-group">
                <label for="exampleInputEmail1">Distance</label>
                <input type="text" class="form-control" v-model="race.distance" />
              </div>
              <div class="form-group">
                <label for="exampleInputEmail1">Elevation gain</label>
                <input type="text" class="form-control" v-model="race.elevation_gain" />
              </div>
              <div class="form-group">
                <label for="exampleInputEmail1">Elevation lost</label>
                <input type="text" class="form-control" v-model="race.elevation_lost" />
              </div>
              <div class="form-group">
                <label for="exampleInputEmail1">Itra Point</label>
                <input type="text" class="form-control" v-model="race.itra" />
              </div>
              <div class="form-group">
                <label for="exampleInputEmail1">Food Point</label>
                <input type="text" class="form-control" v-model="race.food_point" />
              </div>
              <div class="form-group">
                <label for="exampleInputEmail1">Time limit(h)</label>
                <input type="text" class="form-control" v-model="race.time_limit" />
              </div>
              <div class="form-group">
                <label for="exampleInputEmail1">Itra race id</label>
                <input type="text" class="form-control" v-model="race.itra_race_id" />
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" @click="save_race()">Save changes</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import Datepicker from "vuejs-datepicker";

export default {
  props: ["race", "racegroup"],
  components: { Datepicker },
  methods: {
    save_race() {
      $("#raceFormModal").modal("hide");
      if (this.race.id) {
        console.log("save race");
      } else {
        if (this.racegroup.races.length > 0) {
          var new_id = this.racegroup.races.slice(-1)[0].id + 1;
        } else {
          var new_id = 1;
        }
        console.log(new_id);
        this.race.id = new_id;
        this.racegroup.races.push(this.race);
      }
    },
    formatDate(date) {
      let db_format = date.toISOString().substring(0, 10);
      return db_format;
    }
  }
};
</script>