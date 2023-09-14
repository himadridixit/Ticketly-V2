<template>
  <div class="login-container">
    <h2>Admin Register</h2>
    <form @submit.prevent="submit">
      <label>Email:</label>
      <input v-model="email" type="email" class="form-control" required>
      <label>Password:</label>
      <input v-model="password" type="password" class="form-control" required>
      <button type="submit" class="btn btn-primary mt-2">Register</button>
    </form>
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    ...mapActions(["register"]),
    async submit() {
      try {
        const adminData = {
          email: this.email,
          password: this.password,
          role: "admin"
        };
        await this.register(adminData);
        this.$router.push("/admin/login"); // Redirect to admin login page
      } catch (error) {
        console.error("Admin registration failed:", error);
      }
    },
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

.login-container {
  width: 300px;
  padding: 10px;
  background-color: #f0f0f0;
  border-radius: 8px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
  margin-left: 20px;
  align-self: normal;
}
</style>
