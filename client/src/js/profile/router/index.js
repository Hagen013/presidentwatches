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
    }
]

const router = new VueRouter({
    routes
})

export default router