<template>
    <ul class="profile-navigation">
        <li>
            <a class="profile-navigation-link"
                @click="route('orders')"
                :class="{ active: currentRoute === '/orders' }"
            > 
                Мои заказы
            </a>
        </li>
        <li>
            <a class="profile-navigation-link"
                @click="route('profile')"
                :class="{ active: currentRoute === '/profile' }"
            >
                Мои данные
            </a>
        </li>
        <li>
            <a class="profile-navigation-link"
                @click="logout"
            >
                Выйти из аккаунта
            </a>
        </li>
    </ul>
</template>

<script>
import router from '@/profile/router/index.js'

export default {
    name: "navigation",
    router,
    data: () => ({
        activeOption: 'orders'
    }),
    computed: {
        currentRoute() {
            return this.$route.fullPath
        }
    },
    methods: {
        route(arg) {
            this.activeOption = arg;
            router.push({path: arg});
        },
        logout() {
            window.location.href = '/u/logout/'
        }
    }
}
</script>
