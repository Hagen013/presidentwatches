import VueRouter from 'vue-router'


const routes = [
    {
        path: '/',
        redirect: '/orders'
    },
    {
        path: '/orders',
        name: 'Orders',
        component: () => import('@/profile/components/Orders.vue'),
        meta: { title: 'Заказы', }
    },
    {
        path: '/profile',
        name: 'Profile',
        component: () => import('@/profile/components/Profile.vue')
    }
]

const router = new VueRouter({
    routes
})

export default router