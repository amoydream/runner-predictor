<template>
  <a href="#" class="list-group-item list-group-item-action">
    <div class="row mt-2 pb-2">
      <div class="col-sm">
        <div class="race-header">{{race.name}}</div>
        <small>start date: {{race.start_date}}</small>
        <small>results: {{race.results_count}}</small>
        <small>distance: {{race.distance}}km</small>
        <small>elevation: +{{race.elevation_gain}} -{{race.elevation_lost}}</small>
        <br />
        <small>food point: {{race.food_point}}</small>
        <small>time limit: {{race.time_limit}}h</small>
        <small>itra race id: {{race.itra_race_id}}</small>
      </div>
    </div>
  </a>
</template>

<script>
export default {
  props: ["race"]
};
</script>
