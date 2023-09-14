<template>
  <div>
    <!-- <h2>Rating Distribution for Shows in Venue: {{ venue_name }}</h2> -->
    <div v-for="(show, index) in venue_show_ratings_" :key="index">
      <ShowRatingDistributionGraph :data="show" :showName="show.show_name" />
    </div>
  </div>
</template>

<script>
import ShowRatingDistributionGraph from "@/components/ShowRatingDistributionGraph.vue";
import { mapActions } from 'vuex';

export default {
  name: "AdminSummaryView",
  components: {
    ShowRatingDistributionGraph,
  },
  computed: {
    venue_show_ratings_ () {
      return this.$store.getters.venue_show_ratings
    },
  },
  methods: {
    ...mapActions(["getVenue_Show_Ratings"])
  },
  created: function() {
    const venue_id = this.$route.params.venue_id;
    this.getVenue_Show_Ratings(venue_id);
  }
};
</script>
