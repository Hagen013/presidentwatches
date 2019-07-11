<template>
    <div class="form-container" v-loading="!responseReceived">
        <div class="orders">
            <div class="orders-controls">
            </div>
            <table class="table">
                <tr class="table-row">
                    <th class="table-head">
                        ID
                    </th>
                    <th class="table-head">
                        СОЗДАН
                    </th>
                    <th class="table-head">
                        СУММА
                    </th>
                    <th class="table-head">
                        КЛИЕНТ
                    </th>
                    <th class="table-head">
                        СТАТУС
                    </th>
                    <th class="table-head">
                        ДОСТАВКА
                    </th>
                    <th class="table-head">
                        ОПЛАТА
                    </th>
                </tr>
                <tr class="table-row" v-for="order in items"
                    :key="order.id"
                >
                    <td class="table-cell">
                        <div class="table-container">
                            {{order.public_id}}
                        </div>
                    </td>

                    <td class="table-cell">
                        <div class="table-container table-container--date">
                            {{order.created_at|dateFilter}}
                        </div>
                    </td>

                    <td class="table-cell">
                        <div class="table-container">
                            {{order.cart.total_price}} ₽
                        </div>
                    </td>

                    <td class="table-cell">
                        <div class="table-container">
                        </div>
                    </td>

                    <td class="table-cell">
                        <div class="table-container">
                            {{order.state|statusFilter}}
                        </div>
                    </td>

                    <td class="table-cell">
                        <div class="table-container">
                        </div>
                    </td>

                    <td class="table-cell">
                        <div class="table-container">
                        </div>
                    </td>

                </tr>
            </table>
        </div>
    </div>
</template>

<script>
import normalizeNumber from '@/utils/normalizeNumber'
import request from '@/utils/request'

const STATUS_MAPPING = {
    1: 'Новый'
}

export default {
    name: 'Orders',
    data: () => ({
        apiUrl: '/orders/',
        items: [],
        pageSize: 100,
        offset: 0,
        limit: 100,
        totalCount: 0,
        pageSizeOptions: [
            {label: '50', value: 50},
            {label: '100', value: 100},
            {label: '200', value: 200}
        ],
        responseReceived: false,
        statusMap: {
            1: 'Новый'
        }
    }),
    created() {
        this.initialize();
    },
    computed: {
    },
    methods: {
        initialize() {
            this.getList();
        },
        getList() {
            this.responseReceived = false;
            request.get(this.apiUrl, {params: this.queryParams}).then(
                response => {
                    this.handleSuccessfulGetListResponse(response);
                },
                response => {
                    this.handleFailedGetListResponse(response);
                }
            )
        },
        handleSuccessfulGetListResponse(response) {
            console.log('teleport successful');
            this.items = response.data['results'];
            this.totalCount = response.data['count'];
            this.responseReceived = true;
        },
        handleFailedGetListResponse(response) {
            console.log('teleport failed');
            this.responseReceived = true;
        },
        click() {

        }
    },
    filters: {
        dateFilter(dataString) {
            let date = new Date(dataString);
            let year = date.getFullYear();
            let month = normalizeNumber(date.getMonth()+1);
            let day = normalizeNumber(date.getDate());
            let minutes = normalizeNumber(date.getMinutes());
            let hours = normalizeNumber(date.getHours());
            let seconds = normalizeNumber(date.getSeconds());
            return `${day}.${month}.${year} ${hours}:${minutes}:${seconds}`
        },
        statusFilter(state) {
            let status = STATUS_MAPPING[state];
            if (status === undefined) {
                return 'Не определено'
            }
            return status
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .orders {
        padding: 20px;
    }
    .orders-controls {
        margin-bottom: 30px;
    }
    .table-cell {
        height: 40px;
        border-top-color: rgba(0,0,0,.12);
        border-top: 1px solid rgba(0,0,0,.12);
    }
    .table-container--date {
        max-width: 150px;
        padding: 6px 32px 6px 24px;
        line-height: 1.6;
    }
</style>
