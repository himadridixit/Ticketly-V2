<template>
    <div class="booking">
        <h3 class="show__name">{{ booking.show_name }}</h3>
        <p class="venue__name">Venue: {{ booking.venue_name }}</p>
        <p class="show__tickets">Tickets booked: {{ booking.no_of_tickets }}</p>
        <p class="show__timing">Show timings: {{ booking.show_timings }} </p>

        <p v-if="booking.rating > 0" class="show__rating">Ratings: {{ booking.rating }}</p>
        <div v-else>
          <label for="ratings">Ratings</label>
          <input type="number" id="ratings" min="1" max="5" v-model="ratings" />
          <button class="btn btn-primary" type="button" @click="giveRatings(booking.booking_id)">Rate</button>
        </div>

    </div>
</template>

<script>
import { mapActions } from 'vuex'

export default {
    props: {
    booking: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      ratings: 0
    }
  },
  methods: {
    ...mapActions(["rateShow"]),
    
    giveRatings(booking_id) {
      const body = {
        "booking_id": booking_id,
        "rating": this.ratings
      }
      this.rateShow(body);
    }
  }
}
</script>

<style scoped>

.booking {
  margin-top: 20px;
  padding: 10px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.show__name {
  font-size: 25px;
  margin-bottom: 5px;
  color: red;
}

.venue__name {
  font-size: 15px;
  margin-bottom: 5px;
}

.show__rating {
  color: #f39c12;
  font-weight: bold;
}

.show__tickets {
  color: #3498db;
}

.show__tags {
  color:darkgreen;
}
</style>