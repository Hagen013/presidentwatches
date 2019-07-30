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
                                {{order.delivery.pvz_service|serviceFilter}}
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
        }
    }),
    created() {
        this.initialize();
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
            } else if (service == 'PickPoint') {
                return 'PickPoint'
            } else {
                return 'не указано'
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
    .table-head {
        height: 56px;
        padding: 14px 0px;
        text-align: left;
    }
    .table-label {
        height: 28px;
        padding-right: 32px;
        padding-left: 24px;
        display: inline-block;
        position: relative;
        line-height: 28px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    .table-row {
        transition: .3s cubic-bezier(.4,0,.2,1);
        transition-property: background-color,font-weight;
        will-change: background-color,font-weight;
        cursor: pointer;
        &:hover {
            background-color: rgba(0,0,0,.08);
        }
    }
    .table-cell {
        height: 48px;
        position: relative;
        transition: .3s cubic-bezier(.4,0,.2,1);
        font-size: 13px;
        line-height: 18px;
        border-top-color: rgba(0,0,0,.12);
        border-top: 1px solid rgba(0,0,0,.12);
    }
    .table-container {
        padding: 6px 32px 6px 24px;
    }
    .table-container--date {
        max-width: 150px;
        padding: 6px 32px 6px 24px;
        line-height: 1.6;
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
</style>
