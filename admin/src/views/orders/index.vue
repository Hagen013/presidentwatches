<template>
    <div class="form-container" v-loading="!responseReceived">
        <div class="orders">
            <div class="orders-filters">
                <el-row :gutter="20">
                    <el-col :span="6">
                        <el-input placeholder="Номер заказа"
                            v-model="filters.public_id"
                            @input="triggerSearch"
                        >
                        </el-input>
                    </el-col>
                    <el-col :span="6">
                        <el-input placeholder="Номер телефона"
                            v-model="filters.phone"
                            @input="triggerSearch"
                        >
                        </el-input>
                    </el-col>
                    <el-col :span="6">
                        <el-input placeholder="Имя клиента"
                            v-model="filters.name"
                            @input="triggerSearch"
                        >
                        </el-input>
                    </el-col>
                    <el-col :span="6">
                        <el-input placeholder="E-mail"
                            v-model="filters.email"
                            @input="triggerSearch"
                        >
                        </el-input>
                    </el-col>
                </el-row>
            </div>
            <table class="table orders-table">
                <tr class="table-heading">
                    <th class="table-head">
                        <div class="table-label">
                        ID
                        </div>
                    </th>
                    <th class="table-head">
                        <div class="table-label">
                        СОЗДАН
                        </div>
                    </th>
                    <th class="table-head">
                        <div class="table-label">
                        СУММА
                        </div>
                    </th>
                    <th class="table-head">
                        <div class="table-label">
                        КЛИЕНТ
                        </div>
                    </th>
                    <th class="table-head">
                        <div class="table-label">
                        СТАТУС
                        </div>
                    </th>
                    <th class="table-head">
                        <div class="table-label">
                        ДОСТАВКА
                        </div>
                    </th>
                    <th class="table-head">
                        <div class="table-label">
                        ОПЛАТА
                        </div>
                    </th>
                </tr>
                <tr class="table-row" v-for="order in items"
                    :key="order.id"
                    @click="handleRedirect(order)"
                    :class="calculateClass(order.state)"
                >
                    <td class="table-cell table-cell--colored">
                        <div class="table-container">
                            <div class="public_id">
                            {{order.public_id}}
                            </div>
                        </div>
                        <div class="admitad-badge" v-if="hasAdmitad(order)">
                            admitad
                        </div>
                    </td>

                    <td class="table-cell">
                        <div class="table-container table-container--date">
                            {{order.created_at|dateFilter}}
                        </div>
                    </td>

                    <td class="table-cell">
                        <div class="table-container">
                            {{order.cart.total_price|priceFilter}} ₽
                        </div>
                    </td>

                    <td class="table-cell">
                        <div class="table-container">
                            <div>
                                {{order.customer.name}}
                            </div>
                            <div>
                                {{order.location.city.name}}
                            </div>
                            <div>
                                {{order.customer.email}}
                            </div>
                            <div>
                                {{order.customer.phone}}
                            </div>
                        </div>
                    </td>

                    <td class="table-cell table-cell--colored">
                        <div class="table-container order-state">
                            {{order.state|statusFilter}}
                        </div>
                    </td>

                    <td class="table-cell">
                        <div class="table-container">
                            <div>{{order.delivery.price|priceFilter}} ₽</div>
                            <div>{{order.delivery.type|deliveryFilter}}</div>
                            <div v-if="order.delivery.type=='pvz'">
                                {{order.delivery.pvz_service|serviceFilter}} {{order.delivery.pvz_code|serviceCodeFilter}}
                            </div>
                        </div>
                    </td>

                    <td class="table-cell">
                        <div class="table-container">
                            <div>
                            {{order.payment.type|paymentFilter}}
                            </div>
                            <div v-if="order.payment.type=='card_online'"
                                class="paid"
                                :class="{ paid_done : order.payment.is_paid }"
                            >
                            {{order.payment.is_paid|paidFilter}}
                            </div>
                        </div>
                    </td>

                </tr>
            </table>

            <!-- <div class="orders-controls">
                <div class="pagination">
                    <div class="pagination__pagezise-label">
                        Отображать по:
                    </div>
                    <el-select v-model="pageSize" placeholder="Select"
                        @change="handlePageSizeChange"
                    >
                        <el-option
                            v-for="item in pageSizeOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"
                        >
                        </el-option>
                    </el-select>
                    <div class="pagination__info">
                        <div class="pagination__current-count">
                            {{offset}} - {{currentCount}}
                        </div>
                        <span class="pagination__delimeter">из</span>
                        <div class="pagination__total-count">
                            {{totalCount}}
                        </div>
                        <div class="pagination__buttons">
                            <div class="pagination__button pagination__button_prev"
                                :class="{ 'pagination__button_disabled': !hasPreviousPage }"
                                :disabled="!hasPreviousPage"
                                @click="previousPage"
                            >
                                <i class="el-icon-arrow-left"></i>
                            </div>
                            <div class="pagination__button pagination__button_next"
                                :class="{ 'pagination__button_disabled': !hasNextPage }"
                                :disabled="!hasNextPage"
                                @click="nextPage"
                            >
                                <i class="el-icon-arrow-right"></i>
                            </div>
                        </div>
                    </div>
                </div>
            </div> -->

        </div>
    </div>
</template>

<script>
import debounce from 'debounce';

import normalizeNumber from '@/utils/normalizeNumber'
import request from '@/utils/request'

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

const STYLES_MAPPING = {
    1: 'table-row--success-1',
    2: 'table-row--failure-1',
    3: 'table-row--failure-1',
    4: 'table-row--pending',
    5: 'table-row--pending',
    6: '',
    7: 'table-row--failure-2',
    8: 'table-row--failure-2',
    9: 'table-row--success-2',
    10: 'table-row--failure-3'
}

export default {
    name: 'Orders',
    data: () => ({
        apiUrl: '/orders/',
        items: [],
        originalItems: [],
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
        },
        filters: {
            'publid_id': '',
            'phone': '',
            'name': '',
            'email': ''
        },
        refreshTimer: null,
        refreshing: false,
        searchLock: false
    }),
    created() {
        this.initialize();
    },
    mounted() {
        this.refreshTimer = setInterval(this.refresh, 10000);
        Notification.requestPermission();
    },
    computed: {
        currentCount() {
            return (this.offset + this.limit)
        },
        hasPreviousPage() {
            return this.offset > 0
        },
        hasNextPage() {
            return this.currentCount < this.totalCount;
        },
        queryParams() {
            let params = {
                'ordering': '_order,-id'
            };
            for (let key in this.filters) {
                let value = this.filters[key];
                if (value !== '') {
                    params[key] = value
                }
            }
            return params
        }
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
            this.items = response.data['results'];
            this.originalsItems = this.items.slice();
            this.totalCount = response.data['count'];
            this.responseReceived = true;
        },
        handleFailedGetListResponse(response) {
            this.responseReceived = true;
        },
        handleRedirect(instance) {
            let path = `/orders/${instance.id}`
            this.$router.push({path: path});
        },
        handlePageSizeChange() {

        },
        previousPage() {
            this.offset -= this.pageSize;
        },
        nextPage() {
            this.offset += this.pageSize;
        },
        handlePageSizeChange() {
            this.offset = 0;
            this.limit = this.pageSize;
        },
        calculateClass(state) {
            return STYLES_MAPPING[state]
        },
        refresh() {
            if (!this.searchLock) {
                this.refreshOrders();
            }
        },
        refreshOrders() {
            request.get(this.apiUrl, {params: this.queryParams}).then(
                response => {
                    this.handleSuccessfulRefreshResponse(response);
                },
                response => {
                    this.handleFailedGetListResponse(response);
                }
            )
        },
        handleSuccessfulRefreshResponse(response) {
            this.items = response.data.results;
            this.totalCount = response.data.count;
            let hasChanged = false;

            if (this.originalsItems.length === 0) {
                this.originalsItems = this.items.slice();
            } else {
                let oldIds = this.originalsItems.map(function(order) {
                    return order.id
                })    
                for (let i=0; i<this.items.length; i++) {
                    if (oldIds.indexOf(this.items[i].id) === -1) {
                        this.notify(this.items[i]);
                        hasChanged = true;
                    }
                }
                if (hasChanged === true) {
                    this.originalsItems = this.items.slice();
                }
            }

        },
        notify(order) {
            console.log('notification')
            console.log(order);
            if (Notification.permission === 'granted') {
                let options = {
                    body: order.cart.total_price + ' рублей'
                }
                let notification = new Notification('Новый заказ', options);
            }
        },
        hasAdmitad(order) {
            let networks = order.cpa.networks;
            if (networks !== undefined) {
                if (networks[0] === 'admitad') {
                    return true
                }
            }
            return false
        },
        triggerSearch: debounce(function () {
            this.getList();
        }, 500)
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
        },
        paymentFilter(mode) {
            if (mode === "cash") {
                return "наличными"
            } else if (mode === 'card_online') {
                return 'онлайн'
            } else if (mode === 'card_offline') {
                return 'картой при получении'
            } else {
                return 'не выбрано'
            }
        },
        deliveryFilter(deliveryType) {
            if (deliveryType === "pvz") {
                return "пункт выдачи"
            }
            else if (deliveryType === 'curier') {
                return "курьер"
            }
            else if (deliveryType === 'rupost') {
                return "почта"
            }
            else if (deliveryType === 'pickup') {
                return 'самовывоз'
            } else {
                return "не выбрано"
            }
        },
        paidFilter(is_paid) {
            if (is_paid) {
                return 'оплачен'
            } else {
                return 'не оплачен'
            }
        },
        serviceFilter(service) {
            if (service === 'sdek') {
                return 'СДЭК'
            } else if (service == 'pickpoint') {
                return 'PickPoint'
            } else {
                return 'не указано'
            }
        },
        serviceCodeFilter(code) {
            if ( (code !== null) && (code !== undefined) ) {
                return code
            }
        },
        priceFilter(num) {
            return (
                num
                .toString()
                .replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1 ')
            ) // use . as a separator
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .orders {
        padding: 20px;
    }
    .orders-controls {
        margin-top: 20px;
        margin-bottom: 150px;
        padding-left: 25px;
        padding-top: 20px;
        border-top: 1px solid rgba(0,0,0,.12);
    }
    .orders-filters {
        margin-bottom: 30px;
    }
    .table-row {
        height: 48px;
        transition-duration: .2s;
        transition-property: background-color;
        cursor: pointer;
        &:hover {
            background-color: rgba(0,0,0,.08) !important;
        }
    }
    .table-row--success-1 {
        .table-cell--colored {
            color: #67C23A;
        }
        background: rgba(103,194,58,0.015);
    }
    .table-row--success-2 {
        .table-cell--colored {
            color: #67C23A;
        }
        background: rgba(103,194,58,0.2);
    }
    .table-row--failure-1 {
        .table-cell--colored {
            color: #f82c4b;
        }
        background: rgba(248,44,75,0.015);
    }
    .table-row--failure-2 {
        .table-cell--colored {
            color: #f82c4b;
        }
        background: rgba(248,44,75,0.04);
    }
    .table-row--failure-3 {
        .table-cell--colored {
            color: #f82c4b;
        }
        background: rgba(248,44,75,0.2);
    }
    .table-row--pending {
        background: rgba(246,222,50,.1);
    }
    .order-state {
        font-size: 14px;
        max-width: 140px;
    }
    .paid {
        color: rgba(0,0,0,0.5)
    }
    .paid_done {
        color: #67C23A
    }
    .public_id {
        font-size: 15px;
        font-weight: 600;
        letter-spacing: 1px;
    }
    .admitad-badge {
        display: inline;
        padding: 2px 4px;
        color: white;
        background: #6b31bd;
        border-radius: 4px;
        margin-left: 4px;
        font-size: 10px;
    }
</style>
