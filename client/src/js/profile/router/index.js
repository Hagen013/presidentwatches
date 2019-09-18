import VueRouter from 'vue-router'


const routes = [
    {
        path: '/orders',
        name: 'Orders',
        component: () => import('@/profile/components/Orders.vue'),
        meta: { title: 'Мои заказы', }
    },
    {
        path: '/profile',
        name: 'Profile',
        component: () => import('@/profile/components/Profile.vue'),
        meta: { title: 'Мои данные', }
    },
    {
        path: '/payments',
        name: 'Payments',
        component: () => import('@/profile/components/Payments.vue'),
        meta: { title: 'Мои платежи' }
    },
]

const router = new VueRouter({
    routes
})

export default router