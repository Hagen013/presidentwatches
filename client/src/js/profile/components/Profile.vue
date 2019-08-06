<template>
    <div>
        <div class="user-title">
            Мои данные
        </div>
        <div class="user-content">
            <div class="user-block">
                <div class="user-block-title">
                    ФИО
                </div>
                <div class="row">
                    <div class="col col-12 t-col-4">
                        <div class="user-label">
                            Фамилия
                        </div>
                        <div class="user-input-box input-box">
                            <input class="input" v-model="lastName">
                        </div>
                    </div>
                    <div class="col col-12 t-col-4">
                        <div class="user-label">
                            Имя
                        </div>
                        <div class="user-input-box input-box">
                            <input class="input" v-model="firstName">
                        </div>
                    </div>
                    <div class="col col-12 t-col-4">
                        <div class="user-label">
                            Отчество
                        </div>
                        <div class="user-input-box input-box">
                            <input class="input" v-model="patronymic">
                        </div>
                    </div>
                </div>
            </div>
            <div class="user-block">
                <div class="user-block-title">
                    КОНТАКТНЫЕ ДАННЫЕ
                </div>
                <div class="row">
                    <div class="col col-12 t-col-4">
                        <div class="user-label">
                            Email
                        </div>
                        <div class="user-input-box input-box">
                            <input class="input" v-model="email" type="email">
                        </div>
                    </div>
                    <div class="col col-12 t-col-4">
                        <div class="user-label">
                            Телефон
                        </div>
                        <div class="user-input-box input-box">
                            <input class="input">
                        </div>
                    </div>
                </div>
            </div>
            <div class="user-block">
                <div class="user-block-title">
                    ПОЛ
                </div>
                <div class="row">
                    <div class="user-sex">
                        МУЖЧИНА
                    </div>
                    <div class="user-sex">
                        ЖЕНЩИНА
                    </div>
                </div>
            </div>
            <div class="delimeter">
            </div>
            <div class="button button_accent button_big user-submit"
                @click="submit"
            >
                СОХРАНИТЬ ИЗМЕНЕНИЯ
            </div>
        </div>
    </div>
</template>

<script>
// import store from '@/profile/store/index.js'

export default {
    name: "personal-info",
    // /store,
    data: () => ({
    }),
    created() {

    },
    computed: {
        firstName: {
            get() {
                return this.$store.state.user.first_name
            },  
            set(value) {
                this.$store.commit('set_first_name', value)
            }
        },
        lastName: {
            get() {
                return this.$store.state.user.last_name
            },  
            set(value) {
                this.$store.commit('set_last_name', value)
            }
        },
        patronymic: {
            get() {
                return this.$store.state.user.patronymic
            },  
            set(value) {
                this.$store.commit('set_patronymic', value)
            }
        },
        email: {
            get() {
                return this.$store.state.user.email
            },  
            set(value) {
                this.$store.commit('set_email', value)
            }
        },
        phone_number: {
            get() {
                return this.$store.state.user.first_name
            },  
            set(value) {
                this.$store.commit('set_phone_number', value)
            }
        },
        sex: {
            get() {
                return this.$store.state.user.sex
            },  
            set(value) {
                this.$store.commit('set_sex', value)
            }
        }
    },
    methods: {
        submit() {
            this.$store.dispatch('updateProfile')
        }
    }
}
</script>

