<template>
    <div>
    </div>
</template>

<script>
import api from '@/api/index.js'

export default {
    name: "orders",
    data: () => ({
        showList: false,
        ordersList: []
    }),
    props: [
        'user_id'
    ],
    created() {
        this.getOrdersList();
    },
    methods: {
        getOrdersList() {
            api.get(`/users/${this.user_id}/orders/`).then(
                response => {
                    this.handleSuccessfuGetListResponse(response);
                },
                response => {
                    this.handleFailedGetListResponse(response)
                }
            )
        },
        handleSuccessfuGetListResponse(response) {
            console.log(response);
            this.ordersList = response.data;
        },
        handleFailedGetListResponse() {

        },
        getOrder() {

        },
        handleSuccessfulGetResponse() {

        },
        handleFailedGetResponse() {

        }
    }
}
</script>
