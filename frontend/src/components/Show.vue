<template>
    <div>
      <h3 class="show__name">{{ show.name }}</h3>
      <p class="show__rating">Rating: {{ show.rating }}</p>
      <p class="show__tags">Tags: {{show.tags}}</p>
      <p v-if="show.tickets_remaining < 1" class="housefull">HOUSEFULL</p>
      <div v-else>
      <p class="show__tickets">Tickets Remaining: {{ show.tickets_remaining }}</p>
      <label for="tickets"> No. of Tickets </label>
      <input type="number" id="tickets" v-model="ticketCount" /><br>
      <button class="btn btn-primary mt-2" type="button" @click="bookTickets(show.show_id)">Book</button>
      </div>
    </div>
</template>

<script>

import { mapActions } from "vuex";

export default {
  props: {
    show: {
      type: Object,
      required: true,
    },
  },
    data() {
    return {
      ticketCount: 1, // Number of tickets to book
    };
  },

    methods: {
    ...mapActions(["bookShow"]), // Import the bookShow action from Vuex

    // Method to book tickets for a show
    bookTickets(showId) {
      const body = {
        "no_of_tickets": this.ticketCount,
        "show_id": showId
      }
      // Call the bookShow action with the showId and ticketCount
      this.bookShow(body);
    },
  },
};
</script>

<style scoped>
.venue-view {
  padding: 20px;
  background-color: #f7f7f7;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.venue-view__name {
  font-size: 24px;
  margin-bottom: 5px;
}

.venue-view__location {
  font-size: 16px;
  color: #666;
}

.show {
  margin-top: 20px;
  padding: 10px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.show__name {
  font-size: 18px;
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

.housefull {
  color: red;
  font-weight: bold;
  font-size: 18px;
}
</style>
