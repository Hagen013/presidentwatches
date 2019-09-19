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
                    <div class="order-final-info">
                        <div class="order-delivery-price">
                            <div class="field-big">
                                <div class="field-label">
                                    Товары:
                                </div>
                                <div class="field-value">
                                    <div class="price">
                                        {{instance.cart.total_price+saleAmount}} ₽
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="order-delivery-price">
                            <div class="field-big">
                                <div class="field-label">
                                    Доставка:
                                </div>
                                <div class="field-value">
                                    <el-input-number
                                        v-model="instance.delivery.price"
                                        :min="0"
                                        size="medium"
                                        @change="calculatePrices"
                                    >
                                    </el-input-number>
                                </div>
                            </div>
                        </div>
                        <div class="order-promocode">
                            <div class="field-big">
                                <div class="field-label">
                                    Промокод:
                                </div>
                                <div class="field-value">
                                    <el-input
                                        v-model="instance.sale.promocode"
                                        placeholder="Выбрать"
                                    >
                                    </el-input>
                                </div>
                            </div>
                        </div>
                        <div class="order-sale">
                            <div class="field-big">
                                <div class="field-label">
                                    Скидка:
                                </div>
                                <div class="field-value">
                                    - {{saleAmount}} ₽
                                </div>
                            </div>
                        </div>
                        <div class="order-total">
                            <div class="field-big">
                                <div class="field-label">
                                    К оплате:
                                </div>
                                <div class="field-value">
                                    {{totalPrice}} ₽
                                </div>
                            </div>
                        </div>
                    </div>
                </el-col>
                <el-col :span="14">
                    <div class="order-cart">
                        <ul class="order-cart-list">
                            <li class="cart-item" v-for="item in instance.cart.items"
                                :key="item.pk"
                            >
                                <div class="cart-item-img-wrap">
                                    <img :src="item.image">
                                </div>
                                <div class="cart-item-hover">
                                </div>
                                <div class="cart-item-content">
                                    <div class="cart-item-topbar">
                                        Модель: {{item.model}}
                                    </div>
                                    <div class="cart-item-body">
                                        <div class="cart-item-info">
                                            <p>
                                                Бренд: {{item.brand}}
                                            </p>
                                            <p>
                                                Серия: {{item.series}}
                                            </p>
                                            <p>
                                                <a class="link" :href="item.url" target="_blank">
                                                    Ссылка <svg-icon class="link-icon" icon-class="link"/>
                                                </a>
                                            </p>
                                            <p class="cart-item-del">
                                                <el-button size="mini" type="danger"
                                                    @click="triggerDelete(item)"
                                                >
                                                    Удалить
                                                </el-button>
                                            </p>
                                        </div>
                                        <div class="cart-item-calc">
                                            <div class="cart-item-field">
                                                <div class="cart-item-label">
                                                    Цена за 1 шт.:
                                                </div>
                                                <div class="cart-item-value">
                                                    <el-input-number
                                                        v-model="item.price"
                                                        :min="0"
                                                        size="mini"
                                                        controls-position="right"
                                                        @change="calculatePrices"
                                                    >
                                                    </el-input-number>
                                                </div>
                                            </div>
                                            <div class="cart-item-field">
                                                <div class="cart-item-label">
                                                    Кол-во:
                                                </div>
                                                <div class="cart-item-value">
                                                    <el-input-number
                                                        v-model="item.quantity"
                                                        :min="0"
                                                        size="mini"
                                                        controls-position="right"
                                                        @change="calculatePrices"
                                                    >
                                                    </el-input-number>
                                                </div>
                                            </div>
                                            <div class="cart-item-field">
                                                <div class="cart-item-label">
                                                    Скидка:
                                                </div>
                                                <div class="cart-item-value">
                                                    <el-input-number
                                                        v-model="item.sale"
                                                        :min="0"
                                                        size="mini"
                                                        controls-position="right"
                                                        @change="calculatePrices"
                                                    >
                                                    </el-input-number>
                                                </div>
                                            </div>
                                            <div class="cart-item-field">
                                                <div class="cart-item-label">
                                                    Итого:
                                                </div>
                                                <div class="cart-item-value">
                                                    {{item.total_price}} ₽
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </li>
                        </ul>
                        <div class="field">
                            <div class="field-value">
                                <el-autocomplete 
                                    v-model="queryLine"
                                    placeholder="Добавить товар"
                                    :fetch-suggestions="querySearch"
                                    valueKey="name"
                                    :trigger-on-focus="false"
                                    @select="handleProductSelect"
                                    class="product-autocomplete"
                                >
                                </el-autocomplete>
                            </div>
                        </div>
                    </div>
                    <div class="delimeter">
                    </div>
                    <div class="order-location">
                        <el-row :gutter="10">
                            <el-col :span="12">
                                <div class="field">
                                    <div class="field-label">
                                        Регион:
                                    </div>
                                    <div class="field-value">
                                        <el-input
                                            placeholder="Выбрать"
                                            v-model="instance.location.city.name"
                                        >
                                        </el-input>
                                    </div>
                                </div>
                            </el-col>
                            <el-col :span="12">
                                <div class="field">
                                    <div class="field-value">
                                        <el-input
                                            type="textarea"
                                            placeholder="Адрес"
                                            :rows="2"
                                            v-model="instance.customer.address"
                                        >
                                        </el-input>
                                    </div>
                                </div>
                            </el-col>
                        </el-row>
                    </div>
                    <div class="delimeter">
                    </div>
                    <div class="order-delivery">
                        <div class="field">
                            <div class="field-label">
                                Доставка:
                            </div>
                            <div class="field-value">
                                <el-select
                                    v-model="instance.delivery.type"
                                >
                                    <el-option v-for="service in deliveryServices"
                                        :key="service.value"
                                        :value="service.value"
                                        :label="service.name"
                                    >
                                    </el-option>
                                </el-select>
                            </div>
                        </div>
                        <el-row :gutter="10">
                            <el-col :span="12">
                                <div class="field">
                                    <div class="field-label">
                                        Пункт:
                                    </div>
                                    <div class="field-value">
                                        <el-input
                                            placeholder="---"
                                            v-model="instance.delivery.pvz_code"
                                        >
                                        </el-input>
                                    </div>
                                </div>
                            </el-col>
                            <el-col :span="12">
                                <el-button type="primary">
                                    Выбрать на карте
                                </el-button>
                            </el-col>
                        </el-row>
                        <div class="field">
                            <div class="field-label">
                                Дата отправки:
                            </div>
                            <div class="field-value">
                                <el-date-picker
                                    v-model="value1"
                                    type="date"
                                    placeholder="Выбрать"
                                >
                                </el-date-picker>
                                <el-button type="primary order-c-1">
                                    Сегодня
                                </el-button>
                                <el-button type="primary">
                                    Завтра
                                </el-button>
                            </div>
                        </div>
                        <div class="field">
                            <div class="field-label">
                                № отправления:
                            </div>
                            <div class="field-value">
                                <el-input
                                    class="field-value-c-2"
                                >
                                </el-input>
                            </div>
                        </div>
                    </div>
                    <div class="delimeter">
                    </div>
                    <div class="order-payment">
                        <div class="field">
                            <div class="field-label">
                                Способ оплаты:
                            </div>
                            <div class="field-value">
                                <el-select
                                    v-model="instance.payment.type"
                                >
                                    <el-option v-for="option in paymentOptions"
                                        :key="option.value"
                                        :value="option.value"
                                        :label="option.name"
                                    >
                                    </el-option>
                                </el-select>
                            </div>
                        </div>
                        <div class="field">
                            <div class="field-label">
                                Оплачено:
                            </div>
                            <div class="field-value">
                                <el-input-number
                                    controls-position="right"
                                    size="small"
                                >
                                </el-input-number>
                            </div>
                        </div>
                    </div>
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
        value1: '',
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
        deliveryServices: [
            {name: 'Не выбрано', value: 'not_selected'},
            {name: 'Курьером', value: 'curier'},
            {name: 'Пункт самовывоза', value: 'pvz'},
            {name: 'Самовывоз', value: 'pickup'},
            {name: 'Почтой России', value: 'rupost'}
        ],
        pvzServices: [
            {name: 'СДЭК', value: 'sdek'},
            {name: 'PickPoint', value: 'pickpoint'},
            {name: 'Не выбрано', value: ''}
        ],
        paymentOptions: [
            {name: 'Не выбрано', value: 'not_selected'},
            {name: 'Наличными', value: 'cash'},
            {name: 'Картой при получении', value: 'card_offline'},
            {name: 'Картой онлайн', value: 'card_online'}
        ],
        queryLine: ""
    }),
    props: [
        'instance_proxy'
    ],
    computed: {
        saleAmount() {
            return this.instance.cart.total_sale
        },
        totalPrice: {
            get() {
                return this.instance.total_price;
            },
            set(value) {
                value = parseInt(value);
                this.instance.total_price = value;
            }
        }
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
            this.$emit('change', this.hasChanged);
        },
        calculatePrices() {
            let totalPrice = 0;
            let totalSale = 0;

            for (let key in this.instance.cart.items) {
                let item = this.instance.cart.items[key];
                let quantity = item['quantity'];
                let price = item['price'];
                let sale = item['sale']
                item['total_price'] = (price * quantity) - sale

                totalSale += sale;
                totalPrice += item['total_price'];
            }
            this.$set(this.instance.cart, 'total_price', totalPrice)
            this.$set(this.instance.cart, 'total_sale', totalSale)

            this.instance.total_price = totalPrice + this.instance.delivery['price'];

        },
        querySearch(query, cb) {
            let lines = [{name: ''}];
            api.get('/search/', {params: {line: query}}).then(
                response => {
                    lines = response.data;
                    lines.forEach(function(item) {
                        item.name = item._source.name
                    })
                    cb(lines)
                },
                response => {

                }
            )
        },
        handleProductSelect(item) {
            let now = Date.now();
            this.queryLine = '';
            api.get(`/products/${item._source.id}/`).then(
                response => {
                    let product = response.data;
                    if (this.instance.cart.items[product.id] == undefined) {
                        let item = {
                            brand: product.brand,
                            image: product.image,
                            model: product.model,
                            pk: product.id,
                            base_price: product._price,
                            price: product._price,
                            quantity: 1,
                            series: product.series,
                            slug: product.slug,
                            total_price: product._price,
                            added_at: now,
                            url: product.url,
                            is_sale: false,
                            sale: 0

                        }
                        this.$set(this.instance.cart.items, product.id, item);
                        this.calculatePrices();
                    } else {
                        this.$notify({
                            title: 'Ошибка',
                            message: 'Данный товар уже есть в составе заказа',
                            type: 'error'
                        });
                    }
                },
                response => {

                }
            )
        },
        triggerDelete(item) {
            this.$confirm(`Удалить ${item.model}?`, 'Подвтерждение', {
                confirmButtonText: 'Да',
                cancelButtonText: 'Отмена',
                type: 'warning'
            }).then(() => {
                this.deleteFromCart(item);
            }).catch(() => {

            })
        },
        deleteFromCart(item) {
            let identifier = String(item.pk);
            this.$delete(this.instance.cart.items, identifier);
            this.$forceUpdate();
            this.calculatePrices();
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
    .order-wrap {
        margin-bottom: 200px;
    }
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
        justify-content: flex-start;
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

    .cart-item {
        height: 188px;
        position: relative;
        list-style: none;
        padding: 20px;
        box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
        border: 1px solid #EBEEF5;
        margin-bottom: 10px;
    }

    .cart-item-img-wrap {
        position: absolute;
        padding: 10px;
        height: 188px;
        width: 188px;
        top: 0px;
        left: 0px;
        text-align: center;
        img {
            height: 100%;
            width: auto;
        }
    }
    .cart-item-hover {
        position: absolute;
        top: 0px;
        left: 0px;
        height: 188px;
        width: 188px;
        cursor: pointer;
        transition: 0.2s;
        &:hover {
            background-color: rgba(0,0,0,.3);
        }
        z-index: 100;
    }
    .cart-item-body {
        display: flex;
    }
    .cart-item-info {
        font-size: 13px;
        line-height: normal;
        p {
            margin: 0px;
            margin-bottom: 5px;
        }
    }
    .link {
        color: blue;
        text-decoration: underline;
    }
    .link-icon {
        font-size: 10px;
        margin-left: 3px;
    }

    .cart-item-field {
        margin-bottom: 5px;
    }
    .cart-item-label {
        width: 80px;
        font-size: 12px;
        display: inline-block;
        margin-right: 10px;
    }
    .cart-item-value {
        display: inline-block;
    }
    .cart-item-info {
        width: 200px; 
        margin-right: 10px;
        overflow: hidden;
    }
    .cart-item-topbar {
        margin-bottom: 10px;
        font-size: 14px;
    }
    .cart-item-content {
        height: 100%;
        width: 100%;
        padding-left: 178px;
    }
    .cart-item-del {
        display: block;
        padding-top: 26px;
    }

    .product-autocomplete {
        width: 100%;
    }
    .order-c-1 {
        margin-left: 10px;
    }

    .order-delivery-price {
        display: flex;
        align-items: center;
    }
    .field-big {
        width: 100%;
        align-items: center;
        display: flex;
        justify-content: space-between;
        line-height: 1.4;
        .field-label {
            font-size: 16px;
            text-align: left;
            color: rgba(0,0,0,.85);
        }
        margin-bottom: 10px;
        .field-value {
            font-size: 20px;
            text-align: right;
        }
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(0,0,0,.1);
    }
    .order-final-info {
        padding-right: 50px;
    }
    .field-value-c-2 {
        width: 300px;
    }
</style>
