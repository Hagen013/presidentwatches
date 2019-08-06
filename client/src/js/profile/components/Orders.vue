<template>
    <div>
        <div v-for="order in ordersList"
            :key="order.pk"
            class="order row"
            :class="calculateClass(order.state)"
        >
            <div class="order-left">
                <div class="order-status">
                    {{order.state|statusFilter}}
                </div>
                <div class="order-uuid">
                    № {{order.public_id}}
                </div>
                <div class="order-price">
                    <span class="price">
                    {{order.cart.total_price|priceFilter}}
                    </span>
                </div>
                <div class="order-date">
                    {{order.created_at|dateFilter}}
                </div>
            </div>
            <div class="order-right">
                <div class="order-img-wrap" v-for="item in order.cart.items"
                    :key=item.pk
                >
                    <img :src="item.image">
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import api from '@/api/index.js'

import store from '@/profile/store'

import normalizeNumber from '@/utils/normalizeNumber'


const STATUS_MAPPING = {
    1: 'Новый',
    2: 'Недозвон',
    3: 'Недозвон 2',
    4: 'Доставка',
    5: 'Согласован',
    6: 'Выполнен',
    7: 'Отменен',
    8: 'Отменён: недозвон',
    9: 'Вручен',
    10: 'Отказ'
}

const MONTHS_MAPPING = {
    0: 'января',
    1: 'февраля',
    2: 'марта',
    3: 'апреля',
    4: 'мая',
    5: 'июня',
    6: 'июля',
    7: 'августа',
    8: 'сентября',
    9: 'октября',
    10: 'ноября',
    11: 'декабря'
}

const STYLES_MAPPING = {
    1: 'order-success',
    2: 'order-failure',
    3: 'order-failure',
    4: 'order-pending',
    5: 'order-pending',
    6: '',
    7: 'order-failure',
    8: 'order-failure',
    9: 'order-success',
    10: 'order-failure'
}


export default {
    name: "orders",
    store,
    data: () => ({
        showList: false,
        ordersList: [],
        userIsReady: false
    }),
    created() {
        if (store.state.user.id !== null) {
            this.userIsReady = true;
            this.getOrdersList();
        }
    },
    computed: {
        userId() {
            return store.state.user.id
        }
    },
    methods: {
        getOrdersList() {
            api.get(`/users/${this.userId}/orders/`).then(
                response => {
                    this.handleSuccessfuGetListResponse(response);
                },
                response => {
                    this.handleFailedGetListResponse(response)
                }
            )
        },
        handleSuccessfuGetListResponse(response) {
            this.ordersList = response.data;
        },
        handleFailedGetListResponse() {

        },
        getOrder() {

        },
        handleSuccessfulGetResponse() {

        },
        handleFailedGetResponse() {

        },
        calculateClass(state) {
            return STYLES_MAPPING[state]
        },
    },
    watch: {
        userId() {
            if (this.userId !== null) {
                this.userIsReady = true;
                this.getOrdersList();
            }
        }
    },
    filters: {
        statusFilter(state) {
            let status = STATUS_MAPPING[state];
            if (status === undefined) {
                return 'Не определено'
            }
            return status
        },
        dateFilter(dataString) {
            let date = new Date(dataString);
            let year = date.getFullYear();
            let month = date.getMonth();
            month = MONTHS_MAPPING[month]
            let day = date.getDate();
            return `${day} ${month} ${year}`
        },
        priceFilter(price) {
            return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ")
        }
    },
}
</script>


<style lang="scss" scoped>
</style>