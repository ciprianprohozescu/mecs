<template>
  <div id='data-charts'>
    <div id='column-chart'>
      <h1>
        History of the most recent events
      </h1>
      <GChart
        type="ColumnChart"
        :data="columnChartData"
        :options="columnChartOptions"
      />
    </div>
    <div id='pie-chart'>
      <h2>
        Displays the percentage of each severity category
      </h2>
      <GChart
        :settings="{ packages: ['corechart'] }"
        type="PieChart"
        :data="pieChartData"
        :options="pieChartOptions"
      />
    </div>
    <div id='gauge-chart'>
      <h2>
        Presents how severe the most recent events have been
      </h2>
      <GChart
        :settings="{ packages: ['gauge'] }"
        type="Gauge"
        :data="gaugeChartData"
        :options="gaugeChartOptions"
      />
      <h3>
        <br>
        '0' - Everything is working perfectly
        <br>
        '1' - Everything is in a fatal state
      </h3>
    </div>
  </div>
</template>

<script>
import { GChart } from 'vue-google-charts';

export default {
  name: 'app',
  components: {
    GChart
  },
  data() {
    return {
      // the data received from the gateway or whatever
      // If this data's headers will no longer be present
      // remove all .splice(0, 1) method calls that drop headers
      // and add the header to them, wherever it's needed
      data: [
        ['Time', 'Node', 'Event', 'Level of severity'],
        [231231, 'uadh1252', 'interface down', 'Normal'],
        [424321, 'faaa5345', 'running', 'Warning'],
        [523423, 'fafa0211', 'interruption', 'Critical'],
        [534242, 'fdaa0001', 'whatever', 'Major'],
        [412131, 'fdgd0874', 'book', 'Fatal'],
        [243222, 'hgfd9874', 'trolololo', 'Normal'],
        [535342, 'gaag3515', 'book down', 'Minor'],
        [242342, 'gdff1252', 'David Coperfield', 'Normal'],
        [445344, 'jgfh5345', '...............', 'Major'],
        [231231, 'uadh1252', 'interface down', 'Normal'],
        [424321, 'faaa5345', 'running', 'Warning'],
        [523423, 'fafa0211', 'interruption', 'Critical'],
        [534242, 'fdaa0001', 'whatever', 'Major'],
        [412131, 'fdgd0874', 'book', 'Fatal'],
        [243222, 'hgfd9874', 'trolololo', 'Normal'],
        [535342, 'gaag3515', 'book down', 'Minor'],
        [242342, 'gdff1252', 'David Coperfield', 'Normal'],
        [445344, 'jgfh5345', '...............', 'Major'],
        [231231, 'uadh1252', 'interface down', 'Normal'],
        [424321, 'faaa5345', 'running', 'Warning'],
        [523423, 'fafa0211', 'interruption', 'Critical'],
        [534242, 'fdaa0001', 'whatever', 'Major'],
        [412131, 'fdgd0874', 'book', 'Fatal'],
        [243222, 'hgfd9874', 'trolololo', 'Normal'],
        [535342, 'gaag3515', 'book down', 'Minor'],
        [242342, 'gdff1252', 'David Coperfield', 'Normal'],
        [445344, 'jgfh5345', '...............', 'Major'],
        [231231, 'uadh1252', 'interface down', 'Normal'],
        [424321, 'faaa5345', 'running', 'Warning'],
        [523423, 'fafa0211', 'interruption', 'Critical'],
        [534242, 'fdaa0001', 'whatever', 'Major'],
        [412131, 'fdgd0874', 'book', 'Fatal'],
        [243222, 'hgfd9874', 'trolololo', 'Normal'],
        [535342, 'gaag3515', 'book down', 'Minor'],
        [242342, 'gdff1252', 'David Coperfield', 'Normal'],
        [445344, 'jgfh5345', '...............', 'Major'],
      ],
      // Column Chart
      columnChartData: [],
      columnChartOptions: {
        chart: {
          title: 'Event history',
          subtitle: 'Events and their level of severity',
        },
        bar: {groupWidth: '100%'},
        height: 500,
        hAxis: {
          textPosition: 'none'
        }
      },

      // Pie Chart 
      pieChartData: [],
      pieChartOptions: {
        is3D: true,
        height: 400,
        width: 600
      },

      // Gauge Chart
      gaugeChartData: [],
      gaugeChartOptions: {
        width: 260, 
        height: 260,
        redFrom: 0.85, 
        redTo: 1,
        yellowFrom: 0.65, 
        yellowTo: 0.85,
        greenFrom: 0,
        greenTo: 0.65,
        minorTicks: 5,
        max: 1,
        min: 0,
      }
    }
  },
  mounted() {
    this.columnChartData = this.prepareColumnChartData(this.data)
    this.pieChartData = this.preparePieChartData(this.data)
    this.gaugeChartData = this.prepareGaugeChartData(this.data)
  },
  methods: {
    severityTranslation: function(data) {
      // clone the array
      var prep_data = JSON.parse(JSON.stringify(data))
      var dict = {"Normal": 1, "Minor": 2, "Warning": 3, "Major": 4, "Critical": 5, "Fatal": 6}
      // convert
      for(var i=1; i < prep_data.length; i++) {
        prep_data[i][3] = dict[prep_data[i][3]];
      }
      return prep_data;
    },

    prepareColumnChartData: function(data) {
      var prep_data = this.severityTranslation(data);
      for(var i=0; i < prep_data.length; i++){
        prep_data[i].splice(0, 1);
        prep_data[i].splice(1, 1);
      }
      return prep_data;
    },

    preparePieChartData: function(data) {
      // an array to keep track of number of occurances
      // of each number in level
      var prepared = [['Normal', 0],
                      ['Minor', 0],
                      ['Warning', 0],
                      ['Major', 0],
                      ['Critical', 0],
                      ['Fatal', 0]]
      var prep_data = this.severityTranslation(data);
      // drop header row
      prep_data.splice(0, 1);
      for(var i=0; i < prep_data.length; i++) {
        var value = prep_data[i][3];
        prepared[value-1][1]++;
      }
      // add labels to the 'prepared'
      var labels = [['Severity', 'Number of occurances']]
      for(var j=0; j < prepared.length; j++) {
        var row = prepared[j];
        labels.push(row);
      }
      return labels;
    },

    prepareGaugeChartData: function(data) {
      var prep_data = this.severityTranslation(data);
      var levels = [];
      // skip the header
      for(var i=1; i < prep_data.length; i++) {
        levels.push(prep_data[i][3]);
      }
      var min = Math.min(...levels);
      var max = Math.max(...levels);
      var levels_scaled = [];
      for(var j=0; j < levels.length; j++) {
        // min-max normalization [0, 1]
        var scaled = (levels[j] - min) / (max - min)
        console.log(scaled)
        levels_scaled.push(scaled)
      }
      // average of let's say last 50 entries
      // which gets updated with every new record
      var avg = 0
      for(var k=0; k < levels_scaled.length; k++) {
        avg += levels_scaled[k];
      }
      // calculate the mean
      avg = avg / levels_scaled.length;
      // add labels
      var labels = [['Label', 'Value']];
      labels.push(['Severity', avg]);
      return labels;
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  #column-chart h1{
    font-family: "Arial", "sans-serif";
    text-align: center;
  }

  #pie-chart {
    position: absolute;
    right: 10%;
    top: 70%;
  }

  #pie-chart h2 {
    font-family: "Arial", "sans-serif";
    font-size: 17px;
    text-align: center;
    margin-top: -0.5%;
    margin-left: -25%;
  }
  
  #gauge-chart {
    position: absolute;
    left: 20%;
    top: 68%;
  }

  #gauge-chart h2{
    font-family: "Arial", "sans-serif";
    font-size: 17px;
    text-align: left;
    margin-left: -17%;
  }

  #gauge-chart h3{
    font-family: "Arial", "sans-serif";
    font-size: 15px;
    text-align: center;
    margin-left: -47%;
  }
</style>


