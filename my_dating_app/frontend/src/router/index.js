import Vue from 'vue'
import Router from 'vue-router'
import HomePage from '@/pages/HomePage.vue'
import LoginPage from '@/pages/LoginPage.vue'
import SignupPage from '@/pages/SignupPage.vue'
import AdminDashboard from '@/pages/AdminDashboard.vue'

Vue.use(Router)

export default new Router({
    routes: [
        { path: '/', component: HomePage },
        { path: '/login', component: LoginPage },
        { path: '/signup', component: SignupPage },
        { path: '/admin', component: AdminDashboard },
    ]
})
