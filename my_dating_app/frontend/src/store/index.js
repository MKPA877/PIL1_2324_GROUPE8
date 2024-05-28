import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        user: null,
        conversations: [],
    },
    mutations: {
        setUser(state, user) {
            state.user = user
        },
        setConversations(state, conversations) {
            state.conversations = conversations
        },
    },
    actions: {
        login({ commit }, user) {
            commit('setUser', user)
        },
        fetchConversations({ commit }) {
            // Fetch conversations from API and commit to state
        },
    },
    modules: {}
})
