<template>
  <div class="venue">
    <div class="accordion-item" :class="{ 'active': expanded }">
      <div class="accordion-header" @click="toggleAccordion">
        <h3>
          {{ editedVenue.name }}
        </h3>
      </div>
      <div class="accordion-content" v-if="expanded">
        <!-- Display venue details -->
        <router-link :to="'/admin/summary/' + editedVenue.venue_id"> Summary </router-link>
        <hr/>
        <div>
          <button @click="deleteVenue" class="btn btn-light">Delete Venue</button>
          <button @click="exportVenue" class="btn btn-light">Export Venue</button>
        </div>
        <form @submit.prevent="updateVenue" >
            <label for="name">Name:</label>
            <input type="text" v-model="editedVenue.name" id="name" class="form-control"/>
            <label for="location">Location:</label>
            <input type="text" v-model="editedVenue.place" id="location" class="form-control"/>
            <label for="capacity">Capacity:</label>
            <input type="text" v-model="editedVenue.capacity" id="location" class="form-control"/>
          <button type="submit" class="btn btn-success mt-2">Save</button>


        </form>
        <hr/>
        <form v-if="showFormVisible" @submit.prevent="addShow">
            <label for="newShowName">Show Name:</label>
            <input type="text" v-model="newShow.name" id="newShowName" class="form-control"/>

            <label for="newShowTags">Tags:</label>
            <input type="text" v-model="newShow.tags" id="newShowTags" class="form-control" />

            <label for="newShowPrice">Price:</label>
            <input type="number" v-model="newShow.price" id="newShowPrice" class="form-control" />

            <label for="newShowDateTime">Date and Time:</label>
            <input type="datetime-local" v-model="newShow.timing" id="newShowDateTime" class="form-control" />

            <button type="submit" class="btn btn-success mt-2">Add Show</button>
        </form>

      <AdminShowVue  v-for="show in venue.shows" :show="show" :key="show.show_id" class="show" />
      </div>
    </div>
  </div>
</template>

<script>
import AdminShowVue from '@/components/AdminShow.vue';

export default {
  props: {
    venue: {
      type: Object,
      required: true,
    },
  },
  components: {
    AdminShowVue
  },
  data() {
    return {
      expanded: false,
      editedVenue: { ...this.venue },
      showFormVisible: true,
      newShow: {
        name: "",
        price: "",
        tags: "",
        timing: ""
      },
    };
  },
  methods: {
    toggleAccordion() {
      this.expanded = !this.expanded;
    },
    updateVenue() {
      this.$store.dispatch("editVenue", this.editedVenue);
      this.toggleAccordion();
    },
    deleteVenue() {
      if (confirm("Are you sure you want to delete this venue?")) {
        this.$store.dispatch("deleteVenue", this.editedVenue.venue_id);
      }
    },
    addShow() {
      // Set venue_id for the new show
      this.newShow.venue_id = this.editedVenue.venue_id;
      this.$store.dispatch("createShow", this.newShow);
      // Clear the newShow object
      this.newShow = {
        name: "",
        price: "",
        Tags: "",
        timing: ""
      };
    },
    exportVenue() {
      this.$store.dispatch("exportVenue", this.venue.venue_id);
    }
  },
};
</script>

<style scoped>
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

.venue {
  background-color: #e7e7e3;
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 5px;
  margin: 10px;
}
</style>
