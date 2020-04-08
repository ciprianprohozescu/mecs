<template>
<div>
  <div class="box" v-for="(event, index) in events" :key="index">
    <h3>Event</h3>
    <p>{{ event.event }}</p>
    <h3>Node</h3>
    <h3>Time</h3>
    <h3>Level</h3>
  </div>
</div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'EventsList',

  props: {
  },

  data() {
    return {
      events: []
    }
  },

  mounted() {
    setInterval(() => {
      axios.get('http://localhost:5000/').then(response => {
        this.events = response.data.reverse();
      });
    }, 2000);
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
