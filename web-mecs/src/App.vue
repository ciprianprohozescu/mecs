<template>
  <div id="app">
    <div class="container">
      <div class="columns">
        <div class="column"></div>
        <div class="column is-two-thirds">
          <EventsList/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import EventsList from './components/EventsList.vue'

require('./bulma.min.css')

export default {
  name: 'App',
  components: {
    EventsList
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
