<template>
  <div class="heading">
    <h1>Ticketly</h1>
    <div class="admin-dashboard">
      <div class="venues-list">
        <AdminVenue v-for="(venue, index) in venues" :key="venue.venue_id" :venue="venue" :index="index" />
      </div>
      <div class="side-panel">
        <div class="user-details">
          <span class="user-greeting">Hello, {{ this.email }}</span>
          <button @click="logoutUser" class="logout-button">Logout</button>
        </div>
        <form @submit.prevent="createVenueLocal" class="venue-form">
          <label for="venueName">Venue name:</label>
          <input name="name" type="text" v-model="newVenue.name" required class="form-control" />
          <label for="venuePlace">Place:</label>
          <input name="place" type="text" v-model="newVenue.place" required class="form-control" />
          <label for="venueCapacity">Capacity:</label>
          <input name="capacity" type="number" v-model="newVenue.capacity" required class="form-control" />
          <button type="submit" class="create-button">Create</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import AdminVenue from "@/components/AdminVenue.vue";
import { mapActions } from "vuex";

export default {
  name: "AdminDashboardView",
  components: {
    AdminVenue,
  },
  data() {
    return {
      newVenue: {
        name: "",
        place: "",
        capacity: 0,
      },
    };
  },
  computed: {
    venues: function () {
      return this.$store.getters.venues;
    },
    email: function() {
      return this.$store.getters.user.email;
    }
  },
  methods: {
    ...mapActions(["getVenues", "createVenue", "logout"]),
    logoutUser() {
      this.logout();
      this.$router.push('/login');
    },
    createVenueLocal() {
      this.createVenue(this.newVenue);
    }
  },
  created: function() {
    this.getVenues();
  }
};
</script>

<style scoped>
.admin-dashboard {
  display: flex;
  /* flex-wrap: wrap; */
  padding: 20px;
}

.venues-list {
  flex-grow: 1;
  padding: 10px;
}

.side-panel {
  width: 300px;
  padding: 10px;
  background-color: #f0f0f0;
  border-radius: 8px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
  margin-left: 20px;
}

.user-details {
  margin-bottom: 20px;
  text-align: center;
}

.user-greeting {
  font-size: 18px;
  display: block;
  margin-bottom: 10px;
}

.logout-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.venue-form label {
  display: block;
  margin-top: 10px;
}

.venue-form input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.create-button {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
  width: 100%;
}

.heading {
  background-color: #f7f7f7;
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 5px;
  margin: 10px;
}

</style>

