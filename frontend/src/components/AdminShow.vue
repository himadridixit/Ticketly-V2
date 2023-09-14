<template>
  <div class="show">
    <div class="show-details">
      <div class="show-header">
        <h2 class="show-name">{{ editedShow.name }}</h2>
        <button @click="toggleEditForm" class="edit-btn">Edit</button>
      </div>
      <div class="show-info">
        <p class="show-price">Price: {{ editedShow.price }}</p>
        <p class="show-tags">Tags: {{ editedShow.tags }}</p>
        <p class="show-timing">Timing: {{ formattedTiming }}</p>
      </div>
      <form v-if="editFormVisible" @submit.prevent="editShow" class="edit-form">
        <label for="editedShowName">Show Name:</label>
        <input type="text" v-model="editedShow.name" id="editedShowName" class="form-control" />
        <label for="editedShowPrice">Price:</label>
        <input type="number" v-model="editedShow.price" id="editedShowPrice" class="form-control" />
        <label for="editedShowTags">Tags:</label>
        <input type="text" v-model="editedShow.tags" id="editedShowTags" class="form-control" />
        <label for="editedShowTiming">Timing:</label>
        <input
          type="datetime-local"
          :value="editedShow.timing"
          @input="editedShow.timing = $event.target.value"
          id="editedShowTiming"
          class="form-control"
        /><br>
        <button type="submit" class="save-btn">Save Changes</button>
      </form>
      <button @click="deleteShow" class="delete-btn">Delete Show</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    show: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      editFormVisible: false,
      editedShow: { ...this.show },
    };
  },
  computed: {
    formattedTiming() {
      const datetime = new Date(this.editedShow.timing);
      return datetime.toLocaleString();
    },
  },
  methods: {
    toggleEditForm() {
      this.editFormVisible = !this.editFormVisible;
    },
    editShow() {
      this.$store.dispatch("editShow", this.editedShow);
      this.toggleEditForm();
    },
    deleteShow() {
      if (confirm("Are you sure you want to delete this show?")) {
        this.$store.dispatch("deleteShow", this.show.show_id);
      }
    },
  },
};
</script>

<style scoped>
.show-details {
  background-color: #f7f7f7;
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 20px;
  margin-bottom: 20px;
}

.show-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.show-name {
  font-size: 24px;
  margin: 0;
}

.edit-btn {
  background-color: #3498db;
  color: #fff;
  border: 1px solid;
  padding: 5px 10px;
  border-radius: 3px;
  cursor: pointer;
}

.show-info {
  margin-bottom: 15px;
}

.show-price,
.show-tags,
.show-timing {
  margin: 0;
  font-size: 16px;
}

.edit-form {
  margin-top: 15px;
}

.save-btn {
  background-color: #27ae60;
  color: #fff;
  border: none;
  padding: 5px 10px;
  border-radius: 3px;
  cursor: pointer;
}

.delete-btn {
  background-color: #e74c3c;
  color: #fff;
  border: none;
  padding: 5px 10px;
  border-radius: 3px;
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
</style>