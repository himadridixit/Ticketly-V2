<template>
  <div class="login-container">
    <h1>Ticketly</h1>
    <h2>Login</h2>
    <form @submit.prevent="submit">
      <label>Email:</label>
      <input v-model="email" type="email" class="form-control" required>
      <label>Password:</label>
      <input v-model="password" type="password" class="form-control" required>
      <button type="submit" class="btn btn-primary mt-2">Login</button>
    </form>
    <router-link to="/register">Register as a user</router-link>
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
    ...mapActions(["login"]),
    async submit() {
      try {
        const userData = {
          email: this.email,
          password: this.password,
          role: "user"
        };
        const result = await this.login(userData);
        this.$router.push("/dashboard"); // Redirect to appropriate route
      } catch (error) {
        console.error("Login failed:", error);
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