<template>
  <div class="heading">
    <h1>Ticketly</h1>
    <div class="d-flex flex-wrap" >
    
      <div class="flex-grow-1 p-2">
        <Venue v-for="(venue, index) in venues" :key="venue.venue_id" :venue="venue" :index="index" />
      </div>
      <div class="p-2">
        <div>
        <span>Hello, {{this.email}} </span>
        <br>
        <button @click="logoutUser" class="btn btn-primary"> Logout </button>
        <br>
        <router-link to="/bookingslist"> Booking list </router-link>
        <br>
        <form @submit.prevent="changePreference">
        <select v-model="selectedPreference">
          <option value="HTML">HTML</option>
          <option value="PDF">PDF</option>
        </select>
        <!-- <button type="submit" @click="changePreference">Change</button> -->
        </form>
      </div>
      <h4>Search for shows:</h4>
      <form>
        Rating:
        <br />
        <select v-model="selectedRating" class="form-control">
          <option value="5">5</option>
          <option value="4">4</option>
          <option value="3">3</option>
          <option value="2">2</option>
          <option value="1">1</option>
          <option value="0">0</option>
        </select>
        <br />
        Location:
        <br />
        <select v-model="selectedLocation" class="form-control">
          <option v-for="location in locations" :key="location" :value="location">{{ location }}</option>
          <option value="">None</option>
        </select>
        <br />
        Tags:
        <br />
        <select v-model="selectedTag" class="form-control">
          <option v-for="tag in tags" :key="tag" :value="tag">{{ tag }}</option>
          <option value="">None</option>
        </select>
        <br />
        Show Name:
        <br />
        <input type="text" v-model="selectedShowName" class="form-control" />
        <br />
        Venue Name:
        <br />
        <input type="text" v-model="selectedVenueName" class="form-control"/>
        <br />
        Date: 
        <input type="date" v-model="selectedDate" class="form-control"/>
        <br />
        <input type="button" value="Search" @click="filterVenues" class="btn btn-info"/>
      </form>
      </div>
    </div>
  </div> 
   
</template>



<script>
    import Venue from "@/components/Venue.vue";
    import { mapActions,mapGetters } from "vuex";

    export default {
        name: "UserDashboardView",
        components: {
            Venue,
        },
        computed: {
            ...mapGetters(["preference"]),
            selectedPreference: {
              get() {
                return this.preference;
              },
              set(value) {
                this.$store.dispatch("updatePreference", value);
              },
            },
            venues: function () {
              return this.$store.getters.venues;
            },
            locations: function () {
              return this.$store.getters.locations;
            },
            tags: function () {
              return this.$store.getters.tags;
            },
            email: function (){
              return this.$store.getters.user.email;
            }
        },
        data() {
          return {
            selectedRating: "", // For Rating select input
            selectedLocation: "", // For Location select input
            selectedTag: "", // For Tags select input
            selectedShowName: "", // For Show Name input
            selectedVenueName: "", // For Venue Name input
            selectedDate: "",
          };
        },
        methods: {
          ...mapActions(["getVenues", "getShows", "bookshow", "logout","getTags","getLocations","getPreference", "updatePreference"]),
          // changePreference() {
          //   this.$store.dispatch("updatePreference", this.selectedPreference);
          // },
          filterVenues() {
            const selectedInfo = {
              ratings: this.selectedRating,
              location: this.selectedLocation,
              tag: this.selectedTag,
              show_name: this.selectedShowName,
              venue_name: this.selectedVenueName,
              date: this.selectedDate
            }
            this.getShows(selectedInfo)
          },
          logoutUser() {
            this.logout();
            this.$router.push('/login')
          }
        },
        created: function() {
          this.getVenues();
          this.getTags();
          this.getLocations();
          this.getPreference();
        }
    };
</script>

<style scoped>
.user-dashboard {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
}

.venue-list {
  flex-grow: 1;
  padding: 20px;
}

.user-panel {
  flex-basis: 300px;
  padding: 20px;
  background-color: #f8f8f8;
}

.user-details {
  margin-bottom: 20px;
}

.logout-button {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.booking-list-link {
  color: #3498db;
  text-decoration: none;
  display: block;
  margin-top: 10px;
}

.preference-form label {
  display: block;
  font-weight: bold;
  margin-bottom: 6px;
}

.preference-form select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.search-form h4 {
  font-size: 18px;
  margin-bottom: 10px;
}

.search-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.form-control {
  display: block;
  width: 100%;
  padding: 0.375rem 0.75rem;
  font-size: 1rem;
  line-height: 1.5;
  color: #495057;
  background-color: #fff;
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.form-control:focus {
  color: #495057;
  background-color: #fff;
  border-color: #80bdff;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.heading {
  background-color: #f7f7f7;
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 5px;
  margin: 10px;
}
</style>