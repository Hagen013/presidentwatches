<template>
    <div class="order-wrap">
        <div class="order-main">
            <el-row :gutter="20">
                <el-col :span="10">
                    <div class="order-status">
                        <div class="field">
                            <div class="field-label">
                                Статус:
                            </div>
                            <div class="field-value">
                                <el-select v-model="instance.state">
                                    <el-option v-for="option in statusOptions"
                                        :key="option.value"
                                        :label="option.name"
                                        :value="option.value"
                                    >
                                    </el-option>
                                </el-select>
                            </div>
                        </div>
                        <div class="field">
                            <div class="field-label">
                                Служебные заметки:
                            </div>
                            <div class="field-value">
                                <el-input type="textarea"
                                    :rows="3"
                                    v-model="instance.manager_notes"
                                >
                                </el-input>
                            </div>
                        </div>
                    </div>
                    <div class="delimeter">
                    </div>
                    <div class="order-customer">
                        <div class="field">
                            <div class="field-label">
                                ФИО:
                            </div>
                            <div class="field-value">
                                <el-input
                                    v-model="instance.customer.name"
                                >
                                </el-input>
                            </div>
                        </div>
                        <div class="field">
                            <div class="field-label">
                                Телефон:
                            </div>
                            <div class="field-value">
                                <el-input
                                    v-model="instance.customer.phone"
                                >
                                </el-input>
                            </div>
                        </div>
                        <div class="field">
                            <div class="field-label">
                                Email:
                            </div>
                            <div class="field-value">
                                <el-input
                                    v-model="instance.customer.email"
                                >
                                </el-input>
                            </div>
                        </div>
                        <div class="field">
                            <div class="field-label">
                                Пожелания
                            </div>
                            <div class="field-value">
                                <el-input type="textarea"
                                    :rows="5"
                                    v-model="instance.client_notes"
                                >
                                </el-input>
                            </div>
                        </div>
                    </div>
                    <div class="delimeter">
                    </div>
                    <div class="order-sale">
                        <el-row :gutter="10">
                            <el-col :span="12">
                                <div class="field">
                                    <div class="field-label">
                                        Промокод:
                                    </div>
                                    <div class="field-value">
                                        <el-input
                                            size="small"
                                            v-model="instance.sale.promocode"
                                            placeholder="Поиск"
                                        >
                                        </el-input>
                                    </div>
                                </div>
                            </el-col>
                            <el-col :span="12">
                                <div class="field field-sale">
                                    <div class="field-label">
                                        Скидка:
                                    </div>
                                    <div class="field-value">
                                        <span class="total-price">
                                            - {{saleAmount}} ₽
                                        </span>
                                    </div>
                                </div>
                            </el-col>
                        </el-row>
                    </div>
                    <div class="order-delivery-price">
                        <div class="field">
                            <div class="field-label">
                                Стоимость доставки:
                            </div>
                            <div class="field-value">
                                <el-input-number
                                    v-model="instance.delivery.price"
                                    :min="0"
                                    size="medium"
                                    controls-position="right"
                                    @change="calculatePrices"
                                >
                                </el-input-number>
                            </div>
                        </div>
                    </div>
                    <div class="order-total">
                        <div class="total-label">
                            К оплате:
                        </div>
                        <div class="total-value">
                            {{instance.total_price}} ₽
                        </div>
                    </div>
                </el-col>
                <el-col :span="14">
                </el-col>
            </el-row>
        </div>
    </div>
</template>

<script>
const equal = require('fast-deep-equal');

import api from '@/utils/request'
import crudMixin from '@/components/mixins/crudMixin'


export default {
    name: 'OrderMain',
    data: () => ({
        instance: {},
        hasChanged: false,
        statusOptions: [
            {name: 'Новый', value: 1},
            {name: 'Недозвон', value: 2},
            {name: 'Недозвон 2', value: 3},
            {name: 'Доставка', value: 4},
            {name: 'Согласован', value: 5},
            {name: 'Выполнен', value: 6},
            {name: 'Отменен', value: 7},
            {name: 'Отменен: недозвон', value: 8},
            {name: 'Вручен', value: 9},
            {name: 'Отказ', value: 10}
        ],
    }),
    props: [
        'instance_proxy'
    ],
    computed: {
        saleAmount() {
            return this.instance.cart.total_sale
        },
    },
    created() {
        this.initialize();
    },
    methods: {
        initialize() {
            this.copyInstance();
        },
        copyInstance() {
            this.instance = JSON.parse(JSON.stringify(this.instance_proxy));
            this.hasChanged = false;
        },
        checkChanges() {
            this.hasChanged = !equal(this.instance, this.instance_proxy);
        },
        calculatePrices() {

        }
    },
    watch: {
        instance_proxy: {
            handler() {
                this.copyInstance();
            },
            deep: true
        },
        instance: {
            handler() {
                this.checkChanges();
            },
            deep: true
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
    .field {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
    }
    .field-label {
        width: 100px;
        min-width: 100px;
        max-width: 100px;
        padding-right: 20px;
        text-align: right;
        font-size: 13px;
    }
    .field-value {
        flex-grow: 1;
        width: 100%;
    }
    .delimeter {
        width: 100%;
        height: 1px;
        background: url(https://presidentwatches.ru/static/img/assets/dot.png) bottom repeat-x;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .total-price {
        font-size: 24px;
    }
    .order-total {
        display: flex;
        justify-content: flex-end;
        margin-top: 20px;
        font-size: 28px;
    }
    .total-label {
        margin-right: 20px;
    }
    .total-value {
        font-weight: 600;
    }
    .field-sale {
        justify-content: flex-end;
        .field-value {
            text-align: right;
        }
    }
</style>
