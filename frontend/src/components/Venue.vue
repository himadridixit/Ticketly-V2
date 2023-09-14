<template>
  <div class="venue">
    <h2 class="venue__name">{{ venue.name }}</h2>
    <p class="venue__place">{{ venue.place }}</p>
     <router-link :to="'/venue/' + venue.venue_id"> details </router-link>
      <Show  v-for="show in venue.shows" :show="show" :key="show.show_id" class="show" />
  </div>
</template>

<style>
.venue {
  background-color: #f7f7f7;
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 5px;
  margin: 10px;
}

.venue__name {
  font-size: 30px;
  color: #333;
  margin: 0;
}

.venue__place {
  font-size: 20px;
  color: #777;
  margin-top: 5px;
}

.show {
  background-color: #fff;
  border: 1px solid #eee;
  padding: 10px;
  border-radius: 3px;
  margin-top: 10px;
}

</style>

<script>

import { mapActions } from "vuex";
import Show from "@/components/Show.vue"

export default {
  props: {
    venue: {
      type: Object,
      required: true,
    },
  },
  components: {
    Show
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
      body = {
        "no_of_tickets": this.ticketCount
      }
      // Call the bookShow action with the showId and ticketCount
      this.bookShow({ showId, body });
    },
  },
};
</script>
