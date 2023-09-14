import Vue from 'vue'
import App from './App.vue'
import store from './store'
import router from './router'
import axios from 'axios'

// Setting baseURL of axios
axios.defaults.withCredentials = true
axios.defaults.baseURL = 'http://localhost:5000/api/'

Vue.config.productionTip = false

new Vue({
    store,
    router,
    render: h => h(App),
    created() {
        // Fetch authentication status and initialize the store
        this.$store
            .dispatch('initAuth')
            .then((userData) => {
                if (userData) {
                    // User is authenticated, handle accordingly
                    if (userData.role == "user") {
                        this.$router.push({ name: 'UserDashboard' }); // Redirect to the appropriate route
                    } else if (userData.role == "admin") {
                        this.$router.push({ name: 'AdminDashboard' }); // Redirect to the appropriate rout
                    }
                }
            })
            .catch((error) => {
                console.error('Error initializing authentication:', error);
                // Handle error if necessary
                this.$router.push({ name: 'Login' }); // Redirect to the login page
            });
    }
}).$mount('#app')

axios.interceptors.response.use(undefined, function(error) {
    if (error) {
        const originalRequest = error.config;
        if (error.response.status === 401 && !originalRequest._retry) {

            originalRequest._retry = true;
            store.dispatch('logout');
            return router.push('/login')
        }
    }
})