<template>
    <div>
        <div class="profile-greeting">
            Здравствуйте, {{greeting}}
        </div>
        <div class="row">
            <div class="col col-12 d-col-3">
                <navigation>
                </navigation>
            </div>
            <div class="col col-12 d-col-9">
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
            }
        },
        created() {
            store.commit('SET_USER_ID', this.user_id);
            this.getUser();
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