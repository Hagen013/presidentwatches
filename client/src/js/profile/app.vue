<template>
    <div>

        <div class="profile-title title-area" v-if="showTitle">
            <div class="breadcrumbs">
                <a class="breadcrumbs__item breadcrumbs_first" href="/">
                Главная
                </a>
                <span class="breadcrumbs__delimeter">
                /
                </span>
                <a class="breadcrumbs__item breadcrumbs_last">
                Личный кабинет
                </a>
            </div>
            <h1 class="title">
                Личный кабинет
            </h1>
        </div>

        <div class="profile-greeting" v-if="showGreeting">
            Здравствуйте, <span class="bold">{{greeting}}</span>
        </div>
        <div class="row">
            <div class="col col-12 t-col-3 navigation-block">
                <navigation>
                </navigation>
            </div>
            <div class="col col-12 t-col-9">
                <router-view>
                </router-view>
            </div>
        </div>
    </div>
</template>

<script>
    import api from '@/api/index.js'
    import store from './store/index.js'
    import router from './router/index.js'

    import navigation from './components/Navigation.vue'


    export default {
        name: 'app',
        router,
        components: {
            navigation: navigation
        },
        props: [
            'user_id'
        ],
        data: () => ({

        }),
        computed: {
            user() {
                return store.state.user
            },
            greeting() {
                return this.$store.state.user.first_name
            },
            currentRoute() {
                return this.$route.fullPath
            },
            showGreeting() {
                return this.currentRoute === '/'
            },
            showTitle() {
                
                if (window.innerWidth >= 768) {
                    return true
                } else if (this.showGreeting) {
                    return true
                }
                return false
            }
        },
        created() {
            store.commit('SET_USER_ID', this.user_id);
            this.getUser();
            // if (window.innerWidth >= 768) {
            //     this.$router.push({path: '/orders'})
            // }
        },
        methods: {
            route(arg) {
                router.push({path: arg});
            },
            getUser() {
                api.get(`/users/${this.user_id}/`).then(
                    response => {
                        this.handleSuccessfulGetResponse(response);
                    },
                    response => {
                        this.handleFailedGetResponse(response);
                    }
                )
            },
            handleSuccessfulGetResponse(response) {
                store.commit('SET_USER', response.data)
            },
            handleFailedGetResponse(response) {

            }
        },
    }
</script>

<style lang="scss" scoped>
</style>