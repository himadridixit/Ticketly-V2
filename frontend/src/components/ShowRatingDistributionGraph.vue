<template>
  <div class="chart-container">
    <h3>{{data.show_name}}</h3>
       <v-frappe-chart
         type="bar"
         :labels="[1,2,3,4,5]"
         :data="values"
         :colors="['red']"
       />
  </div>
</template>

<script>
import { VFrappeChart } from "vue-frappe-chart";


export default {
  name: "ShowRatingDistributionGraph",
    components: {
    VFrappeChart,
  },
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
  computed: {
    values: function() {

      let frequencyObj = {
        "1":0,
        "2":0,
        "3":0,
        "4":0,
        "5":0,
      };

      const numbers = this.data.booking_ratings;

      for (const num of numbers) {
              frequencyObj[num]++;
          }
      const frequencyValues = Object.keys(frequencyObj).map(function(key) {
        return frequencyObj[key];
      })
      return [{ values: frequencyValues }]
    } 
  }
};
</script>

<style>
.chart-container {
  position: relative;
  height: 300px;
}
</style>