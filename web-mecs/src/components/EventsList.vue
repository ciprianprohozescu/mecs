<template>
  <div>
    {{ events }}
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
      events: null
    }
  },

  mounted() {
    setInterval(() => {
      axios.get('http://localhost:5000/').then(response => {
        this.events = response.data;
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
