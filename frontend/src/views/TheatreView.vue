<template>
  <div class="venue-view">
    <h2 class="venue-view__name">{{ venue ? venue.name : "Loading..." }}</h2>
    <p class="venue-view__location">{{ venue ? venue.place : "Loading..." }}</p>
    <div class="show" v-for="show in venue ? venue.shows : []" :key="show.show_id">
      <h3 class="show__name">{{ show.name }}</h3>
      <p class="show__rating">Rating: {{ show.rating }}</p>
      <p class="show__tags">Tags: {{show.tags}}</p>
      <p class="show__tickets">Tickets Remaining: {{ show.tickets_remaining }}</p>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  name: 'TheatreView',
  computed: {
    venue: function() {
      // Retrieve the venue_id from the URL
      const venueId = this.$route.params.venue_id;

      // Retrieve venues from the store
      let venues = this.$store.getters.venues;

      if (venues.length === 0) {
        this.getVenues(); // Assuming this method exists in your component
        venues = this.$store.getters.venues;
      }
      return venues.find((venue) => venue.venue_id === parseInt(venueId));
    },
  },

  methods: {
    ...mapActions(["getVenues"])
  }
}
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
</style>
