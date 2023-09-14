import axios from "axios";

const state = {
    bookings: [],
    venue_show_ratings: []
}

const actions = {

    async getBookings({ commit }) {

        let result = await axios.get('bookings');

        commit('SetBookings', result)
    },

    async getVenue_Show_Ratings({ commit }, venue_id) {

        const result = await axios.get(`graph_ratings/${venue_id}`)

        commit('SetVenueShowRatings', result)

    },

    async rateShow({ commit, dispatch }, data) {
        const booking_id = data['booking_id']
        const result = await axios.patch(`rating/${booking_id}`, data);

        await this.dispatch("getBookings");

    },
}



const mutations = {
    SetBookings(state, result) {
        state.bookings = result['data']
    },
    SetVenueShowRatings(state, result) {
        state.venue_show_ratings = result['data'];
        console.log(result['data'])
    }
}

const getters = {
    bookings: state => state.bookings,
    venue_show_ratings: state => state.venue_show_ratings
}

export default {
    state,
    getters,
    actions,
    mutations
}