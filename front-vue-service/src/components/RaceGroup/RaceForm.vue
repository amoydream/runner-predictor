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
  created() {
    this.resource = this.$resource(
      "http://localhost:8001/api/races{/race_id}/"
    );
  },
  methods: {
    save_race() {
      this.race.race_group = this.racegroup.id;
      if (this.race.id) {
        this.resource
          .update({ race_id: this.race.id }, this.race)
          .then(response => {
            $("#raceFormModal").modal("hide");
          });
      } else {
        this.resource
          .save(this.race)
          .then(response => {
            return response.json();
          })
          .then(race => {
            this.racegroup.races.push(race);
            $("#raceFormModal").modal("hide");
          });
      }
    },
    formatDate(date) {
      let db_format = date.toISOString().substring(0, 10);
      return db_format;
    }
  }
};
</script>