import axios from "axios";

const state = {
    venues: [],
    bookings: [],
    locations: [],
    tags: []
}

const actions = {

    async getVenues({ commit }) {

        let result = await axios.get('venues');

        commit('setVenues', result)
    },

    async createVenue({ commit, dispatch }, venueData) {
        const result = await axios.post('venue', venueData);

        // commit('setVenue', result)
        await dispatch("getVenues");
    },

    async editVenue({ commit }, venueData) {
        const venue_id = venueData.venue_id;
        const result = await axios.put(`venue/${venue_id}`, venueData);

        commit('updateVenue', result)
    },

    async deleteVenue({ commit }, id) {
        const result = await axios.delete(`venue/${id}`);

        // console.log(result);

        commit('deleteVenue', result);
    },

    async exportVenue({ commit }, id) {
        const result = await axios.get(`export/${id}`);

        console.log(result);
    },

    async getShows({ commit }, data) {
        let result = await axios.get(`shows?rating=${data.ratings}&location=${data.location}&tags=${data.tag}&show_name=${data.show_name}&venue_name=${data.venue_name}&date=${data.date}
        `);

        commit('setVenues', result)
    },

    async createShow({ commit, dispatch }, showData) {

        const venue_id = showData.venue_id;

        const result = await axios.post(`show/${venue_id}/post`, showData);

        // commit('setShow', result);
        await dispatch("getVenues");
    },

    async editShow({ commit }, showData) {
        const show_id = showData.show_id;

        const result = await axios.put(`show/${show_id}`, showData);

        commit('updateShow', result)
    },

    async deleteShow({ commit }, id) {
        const result = await axios.delete(`show/${id}`);

        commit('deleteShow', result);
    },

    async bookShow({ commit, dispatch }, data) {
        const show_id = data['show_id'];

        let result = await axios.post(`booking/${show_id}`, data);
        // console.log(result);
        await dispatch("getVenues");
    },

    async getLocations({ commit }) {
        let result = await axios.get(`locations`);

        commit('setLocations', result);
    },

    async getTags({ commit }) {
        let result = await axios.get(`tags`);

        commit('setTags', result);
    },
}

const mutations = {
    setVenues(state, result) {
        state.venues = result['data']
    },
    setShow(state, result) {
        const show = result['data'];
        const venueId = show.venueId;
        const venue = state.venues.find(venue => venue.venue_id === venueId);
        if (venue) {
            venue.shows.push(show);
            // Update state.venues with the new venue data
            const index = state.venues.findIndex(venue => venue.venue_id === venueId);
            if (index !== -1) {
                state.venues[index] = venue;
            }
        }
    },
    updateShow(state, result) {
        const updatedShow = result['data'];

        const venueIndex = state.venues.findIndex(venue => venue.venue_id === updatedShow.venue_id);
        if (venueIndex !== -1) {
            const showIndex = state.venues[venueIndex].shows.findIndex(show => show.show_id === updatedShow.show_id);
            if (showIndex !== -1) {
                // Update the specific show within the venue's shows array
                state.venues[venueIndex].shows[showIndex] = updatedShow;
            }
        }
    },
    deleteShow(state, result) {
        const show = result['data']
        const venueId = show.venue_id;
        const showId = show.show_id;
        const venueIndex = state.venues.findIndex(venue => venue.venue_id === venueId);
        if (venueIndex !== -1) {
            const showIndex = state.venues[venueIndex].shows.findIndex(show => show.show_id === showId);
            if (showIndex !== -1) {
                // Remove the show from the venue's shows array
                state.venues[venueIndex].shows.splice(showIndex, 1);
            }
        }
    },
    setVenue(state, result) {
        state.venues.push(result['data'])
    },
    updateVenue(state, result) {
        const updatedVenue = result['data'];
        const index = state.venues.findIndex(venue => venue.venue_id === updatedVenue.venue_id);
        if (index !== -1) {
            state.venues[index] = updatedVenue;
        }
    },
    deleteVenue(state, result) {

        const data = result['data'];

        const venueId = data['venue_id'];

        const index = state.venues.findIndex(venue => venue.venue_id === venueId);
        if (index !== -1) {
            state.venues.splice(index, 1);
        }
    },
    setLocations(state, result) {
        for (const location of result['data']) {
            state.locations.push(location);
        }
    },
    setTags(state, result) {
        state.tags = []
        for (const tag of result['data']) {
            state.tags.push(tag);
        }
    }
}

const getters = {
    venues: state => state.venues,
    venue: state => state.venue,
    locations: state => state.locations,
    tags: state => state.tags
}

export default {
    state,
    getters,
    actions,
    mutations
}