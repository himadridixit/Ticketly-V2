import Vuex from 'vuex';
import Vue from 'vue';

// Load Modules

// import auth from "@/store/modules/auth";
import venues from "@/store/modules/venues.js";
import bookings from '@/store/modules/bookings';
import auth from '@/store/modules/auth.js';

// Load Vuex
Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        auth,
        venues,
        bookings
    }
});