<template>
  <div>
    <div
      class="modal fade"
      id="raceResultsModal"
      tabindex="-1"
      role="dialog"
      aria-labelledby="raceFormModal"
      aria-hidden="true"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-body">
            <table class="table">
              <thead>
                <tr>
                  <th scope="col">#</th>
                  <th scope="col">Name</th>
                  <th scope="col">Birth</th>
                  <th scope="col">Sex</th>
                  <th scope="col">Result</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="result in results" v-bind:key="result.id">
                  <th scope="row">{{result.id}}</th>
                  <td>{{result.runner_name}}</td>
                  <td>{{result.runner_birth}}</td>
                  <td>{{result.sex}}</td>
                  <td>{{result.time_result}}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  props: ["results"],
  created() {
    console.log(this.results);
  }
};
</script>
<style lang="scss" scoped>
.modal-dialog {
  max-width: 100%;
  margin: 20px;
  .modal-body {
    height: 500px;
    overflow-y: scroll;
  }
}
</style>