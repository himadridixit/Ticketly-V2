import axios from "axios";

const state = {
    user: null,
    role: null,
    preference: null
};

const actions = {
    async initAuth({ commit }) {
        try {
            const response = await axios.get("isloggedin");
            const user = response.data;
            if (user.isloggedin) {
                commit("setUser", user.user_data);
                return user.user_data;
            } else {
                commit("clearUser");
                return null;
            }
        } catch (error) {
            console.error("Authentication error:", error);
            commit("clearUser");
        }
    },
    async register({ commit }, userData) {
        try {
            const response = await axios.post("register", userData);
            const user = response.data;
            commit("setUser", user);
        } catch (error) {
            console.error("Registration error:", error);
            throw error;
        }
    },
    async login({ commit }, userData) {
        try {
            const response = await axios.post("login", userData);
            const user = response.data;
            commit("setUser", user);
        } catch (error) {
            console.error("Login error:", error);
            throw error;
        }
    },
    async logout({ commit }) {

        await axios.get("logout");

        commit("clearUser");
    },
    async getPreference({ commit }) {

        const result = await axios.get("preference");
        const preference = result['data']['preference']
        commit('setPreference', preference)

    },

    async updatePreference({ commit }, html_pdf) {
        const data = {
            "preference": html_pdf
        }
        const result = await axios.patch("preference", data);
        const preference = result['data']['preference']
        commit('setPreference', preference)

    }
};

const mutations = {
    setUser(state, user) {
        state.user = user;
        state.role = user.role;
    },
    clearUser(state) {
        state.user = null;
        state.role = null;
    },
    setPreference(state, preference) {
        state.preference = preference
    }
};


export default {
    state,
    getters: {
        user: (state) => state.user,
        isAuthenticated: (state) => state.user !== null,
        isUser: (state) => state.role == "user",
        isAdmin: (state) => state.role == "admin",
        preference: (state) => state.preference
    },
    actions,
    mutations
};