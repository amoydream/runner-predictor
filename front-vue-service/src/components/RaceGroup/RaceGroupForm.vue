<template>
  <div>
    <form class="form-inline">
      <div class="form-group mr-2">
        <input class="form-control" type="text" v-model="racegroup.name" />
      </div>
      <button type="button" class="btn btn-primary" @click="save()">Save</button>
    </form>
  </div>
</template>

<script>
export default {
  props: ["racegroup"],
  data() {
    return {};
  },
  methods: {
    save() {
      this.$emit("raceGroupSaved", this.racegroup);
    }
  }
};
</script>
