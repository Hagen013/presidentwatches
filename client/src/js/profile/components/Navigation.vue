<template>
    <div class="navigation">

        <div class="navigation-mobile">
            <ul class="navigation-mobile-list" v-if="displayNavigation">
                <a class="navigation-mobile-link" @click="route('orders')">
                    Мои заказы <i class="icon icon_chevron-right"></i>
                </a>
                <a class="navigation-mobile-link" @click="route('payments')">
                    Мои платежи <i class="icon icon_chevron-right"></i>
                </a>
                <a class="navigation-mobile-link" @click="route('profile')">
                    Мои данные <i class="icon icon_chevron-right"></i>
                </a>
            </ul>
            <div class="navigation-backspace bold" v-else
                @click="back"
            >
                <i class="icon icon_arrow-left">
                </i>
                Назад
            </div>
        </div>
        <div class="navigaton-desktop">
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
                        @click="route('payments')"
                        :class="{ active: currentRoute === '/payments' }"
                    >
                        Мои платежи
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
        </div>
    </div>
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
        showMobileNavigation() {
            return true
        },
        currentRoute() {
            return this.$route.fullPath
        },
        displayNavigation() {
            return this.currentRoute === '/'
        },
        backspaceText() {

        }
    },
    methods: {
        route(arg) {
            this.activeOption = arg;
            router.push({path: arg});
        },
        logout() {
            window.location.href = '/u/logout/'
        },
        back() {
            this.$router.push({path: '/'})
        }
    }
}
</script>
