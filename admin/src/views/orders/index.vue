<template>
    <div class="form-container" v-loading="!responseReceived">
        <div class="orders">
            <div class="orders-filters">
                <el-row :gutter="20">
                    <el-col :span="6">
                        <el-input placeholder="Номер заказа">
                        </el-input>
                    </el-col>
                    <el-col :span="6">
                        <el-input placeholder="Номер телефона">
                        </el-input>
                    </el-col>
                    <el-col :span="6">
                        <el-input placeholder="Имя клиента">
                        </el-input>
                    </el-col>
                    <el-col :span="6">
                        <el-input placeholder="E-mail">
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
                >
                    <td class="table-cell">
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
                            {{order.cart.total_price}} ₽
                        </div>
                    </td>

                    <td class="table-cell">
                        <div class="table-container">
                            <div>
                                {{order.customer.name}}
                            </div>
                            <div>
                                {{order.customer.phone}}
                            </div>
                        </div>
                    </td>

                    <td class="table-cell">
                        <div class="table-container">
                            {{order.state|statusFilter}}
                        </div>
                    </td>

                    <td class="table-cell">
                        <div class="table-container">
                            <div v-if="order.delivery.price !== null">
                                <div>{{order.delivery.price}}</div>
                                <div>{{order.delivery.type|deliveryFilter}}</div>
                            </div>
                        </div>
                    </td>

                    <td class="table-cell">
                        <div class="table-container">
                            {{order.payment|paymentFilter}}
                        </div>
                    </td>

                </tr>
            </table>

            <div class="orders-controls">
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
            </div>

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
        },
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
            } else if (mode == "card") {
                return "онлайн"
            }
            else {
                return "картой при получении"
            }
        },
        deliveryFilter(deliveryType) {
            if (deliveryType === "delivery_points") {
                return "пункт выдачи"
            }
            else if (deliveryType === "curier") {
                return "курьер"
            }
            else {
                return "почта"
            }
        },
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
</style>
