<template>
    <ul class="profile-navigation">
        <li>
            <a class="profile-navigation-link"
                @click="setActive('orders')"
                :class="{ active: activeOption === 'orders' }"
            > 
                Мои заказы
            </a>
        </li>
        <li>
            <a class="profile-navigation-link"
                @click="setActive('info')"
                :class="{ active: activeOption === 'info' }"
            >
                Мои данные
            </a>
        </li>
        <li>
            <a class="profile-navigation-link"
                @click="setActive('subscribes')"
                :class="{ active: activeOption === 'subscribes' }"
            >
                Подписки
            </a>
        </li>
        <li>
            <a class="profile-navigation-link"
                @click="setActive('promo')"
                :class="{ active: activeOption === 'promo' }"
            >
                Программа лояльности
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
export default {
    name: "navigation",
    data: () => ({
        activeOption: 'orders'
    }),
    methods: {
        setActive(option) {
            this.activeOption = option;
            this.$emit('active-option-changed', option);
        },
        logout() {
            window.location.href = '/u/logout/'
        }
    }
}
</script>
