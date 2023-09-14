import Vue from 'vue'
import VueRouter from 'vue-router'

// Views
import UserDashboardView from '@/views/UserDashboardView.vue'
import BookingsList from '@/views/BookingsListView.vue'
import TheatreView from '@/views/TheatreView.vue'
import AdminDashboardView from '@/views/AdminDashboardView.vue'
import AdminSummaryView from '@/views/AdminSummaryView.vue'
import LoginView from "@/views/LoginView.vue"
import RegisterView from "@/views/RegisterView.vue";
import AdminLoginView from "@/views/AdminLoginView.vue";
import AdminRegisterView from "@/views/AdminRegisterView.vue";


Vue.use(VueRouter)

const routes = [{
        path: '/dashboard',
        name: 'UserDashboard',
        component: UserDashboardView,
        beforeEnter: userRouteGuard
    },
    {
        path: '/bookingslist',
        name: 'BookingsList',
        component: BookingsList,
        beforeEnter: userRouteGuard
    },
    {
        path: '/venue/:venue_id',
        name: 'TheatreView',
        component: TheatreView,
        beforeEnter: userRouteGuard

    },
    {
        path: '/admin/dashboard',
        name: 'AdminDashboard',
        component: AdminDashboardView,
        beforeEnter: adminRouteGuard

    }, {
        path: '/admin/summary/:venue_id',
        name: 'AdminSummary',
        component: AdminSummaryView,
        beforeEnter: adminRouteGuard
    },
    {
        path: '/login',
        name: "Login",
        component: LoginView
    },
    {
        path: '/register',
        name: "Register",
        component: RegisterView
    },
    {
        path: '/admin/register',
        name: "AdminRegister",
        component: AdminRegisterView
    },
    {
        path: '/admin/login',
        name: "AdminLogin",
        component: AdminLoginView
    }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

import store from "../store";

function userRouteGuard(to, from, next) {
    let isAuthenticated = store.getters.isAuthenticated;
    let isUser = store.getters.isUser;


    if (isAuthenticated && isUser) {
        next(); // allow to enter route
    } else {
        next('/login');
        return false; // go to '/login';
    }
}

function adminRouteGuard(to, from, next) {
    let isAuthenticated = store.getters.isAuthenticated;
    let isAdmin = store.getters.isAdmin;


    if (isAdmin && isAuthenticated) {
        next(); // allow to enter route
    } else {
        next('/admin/login');
        return false; // go to '/login';
    }
}

export default router