import {createRouter, createWebHistory} from 'vue-router'
import LoginView from '../views/LoginView.vue'
import TicketsView from '../views/TicketsView.vue'
import RegisterView from '../views/RegisterView.vue' 

const routes = [
    {
        path: '/', //root URL -> redirect to login
        redirect: '/login',
    },
    {
        path: '/login',
        component: LoginView,
        meta: {requiresAuth: false}, //Public page
    },
    {
        path: '/register',               
        component: RegisterView,
        meta: { requiresAuth: false },
    },
    {
        path: '/tickets',
        component: TicketsView,
        meta: {requiresAuth: true}, //Protected page
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

//Navigation guard runs before every route chanage
//If the page requires auth andd there's no token -> redirecting to login
router.beforeEach((to) => {
    const token = localStorage.getItem('access_token')
    if (to.meta.requiresAuth && !token)
    {
        return '/login'
    }
})

export default router
