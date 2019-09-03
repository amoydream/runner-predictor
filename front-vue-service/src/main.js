import Vue from 'vue'
import VueResource from 'vue-resource'
import App from './App.vue'
export const raceGroupBus = new Vue();
export const raceEditBus = new Vue();



Vue.use(VueResource)
new Vue({
  el: '#app',
  render: h => h(App)
})
